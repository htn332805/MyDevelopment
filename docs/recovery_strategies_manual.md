# recovery_strategies.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/errors/recovery_strategies.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T14:43:53.262642  
**File Size:** 37,171 bytes  

## Description
Framework0 Foundation - Recovery Automation Strategies

Automated recovery strategies and resilience patterns implementation:
- Configurable retry logic with exponential backoff and jitter
- Circuit breaker pattern for service protection and recovery
- Context-aware fallback execution paths with graceful degradation
- Transaction-style rollback for multi-step operations with dependency tracking
- Recovery workflow orchestration with Framework0 integration

This module provides the "response" side of error management, executing
recovery strategies when errors occur and managing the recovery lifecycle.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: add_retry_exception**
3. **Function: set_retry_condition**
4. **Function: should_retry**
5. **Function: calculate_delay**
6. **Function: execute_with_retry**
7. **Function: get_stats**
8. **Function: __init__**
9. **Function: state**
10. **Function: is_closed**
11. **Function: is_open**
12. **Function: is_half_open**
13. **Function: _can_attempt_call**
14. **Function: _transition_to_half_open**
15. **Function: _handle_success**
16. **Function: _handle_failure**
17. **Function: call**
18. **Function: get_stats**
19. **Function: __init__**
20. **Function: add_fallback**
21. **Function: execute_with_fallback**
22. **Function: get_stats**
23. **Function: __init__**
24. **Function: _initialize_default_strategies**
25. **Function: recover_from_error**
26. **Function: _select_recovery_strategy**
27. **Function: _execute_retry_recovery**
28. **Function: _execute_circuit_breaker_recovery**
29. **Function: _execute_fallback_recovery**
30. **Function: _execute_combined_recovery**
31. **Function: get_stats**
32. **Function: get_logger**
33. **Function: protected_operation**
34. **Class: BackoffStrategy (0 methods)**
35. **Class: CircuitState (0 methods)**
36. **Class: RetryResult (0 methods)**
37. **Class: RetryStrategy (7 methods)**
38. **Class: CircuitBreaker (11 methods)**
39. **Class: FallbackStrategy (4 methods)**
40. **Class: RecoveryOrchestrator (9 methods)**

## Functions (33 total)

### `__init__`

**Signature:** `__init__(self, max_attempts: int, backoff_strategy: BackoffStrategy, initial_delay: float, max_delay: float, backoff_multiplier: float, jitter_factor: float) -> None`  
**Line:** 102  
**Description:** Initialize retry strategy with configuration.

Args:
    max_attempts: Maximum number of retry attempts
    backoff_strategy: Strategy for calculating retry delays
    initial_delay: Initial delay before first retry (seconds)
    max_delay: Maximum delay between retries (seconds)
    backoff_multiplier: Multiplier for exponential backoff
    jitter_factor: Random jitter factor (0.0-1.0) for jitter strategies

### `add_retry_exception`

**Signature:** `add_retry_exception(self, exception_type: type) -> None`  
**Line:** 145  
**Description:** Add exception type that should trigger retry.

Args:
    exception_type: Exception class to retry on

### `set_retry_condition`

**Signature:** `set_retry_condition(self, condition: Callable[[Exception], bool]) -> None`  
**Line:** 155  
**Description:** Set custom retry condition function.

Args:
    condition: Function that takes an exception and returns bool

### `should_retry`

**Signature:** `should_retry(self, exception: Exception, attempt: int) -> bool`  
**Line:** 164  
**Description:** Determine if operation should be retried.

Args:
    exception: Exception that occurred
    attempt: Current attempt number
    
Returns:
    True if should retry, False otherwise

### `calculate_delay`

**Signature:** `calculate_delay(self, attempt: int) -> float`  
**Line:** 193  
**Description:** Calculate delay for retry attempt based on backoff strategy.

Args:
    attempt: Current attempt number (0-based)
    
Returns:
    Delay in seconds before next retry

### `execute_with_retry`

**Signature:** `execute_with_retry(self, operation: Callable) -> RetryResult`  
**Line:** 223  
**Description:** Execute operation with retry logic.

Args:
    operation: Function to execute with retry
    *args: Arguments for the operation
    error_context: Optional error context for Framework0 integration
    **kwargs: Keyword arguments for the operation
    
Returns:
    RetryResult containing execution details and final outcome

### `get_stats`

**Signature:** `get_stats(self) -> Dict[str, Any]`  
**Line:** 332  
**Description:** Get retry execution statistics.

Returns:
    Dictionary containing retry statistics

### `__init__`

**Signature:** `__init__(self, failure_threshold: int, recovery_timeout: float, half_open_max_calls: int, name: str) -> None`  
**Line:** 353  
**Description:** Initialize circuit breaker with configuration.

Args:
    failure_threshold: Number of failures before opening circuit
    recovery_timeout: Time to wait before testing recovery (seconds)
    half_open_max_calls: Maximum calls allowed in half-open state
    name: Name for identification and logging

### `state`

**Signature:** `state(self) -> CircuitState`  
**Line:** 395  
**Description:** Get current circuit state.

### `is_closed`

**Signature:** `is_closed(self) -> bool`  
**Line:** 400  
**Description:** Check if circuit is closed (normal operation).

### `is_open`

**Signature:** `is_open(self) -> bool`  
**Line:** 405  
**Description:** Check if circuit is open (failing fast).

### `is_half_open`

**Signature:** `is_half_open(self) -> bool`  
**Line:** 410  
**Description:** Check if circuit is half-open (testing recovery).

### `_can_attempt_call`

**Signature:** `_can_attempt_call(self) -> bool`  
**Line:** 414  
**Description:** Check if call can be attempted in current state.

Returns:
    True if call can be attempted, False otherwise

### `_transition_to_half_open`

**Signature:** `_transition_to_half_open(self) -> None`  
**Line:** 442  
**Description:** Transition circuit to half-open state.

### `_handle_success`

**Signature:** `_handle_success(self) -> None`  
**Line:** 450  
**Description:** Handle successful call execution.

### `_handle_failure`

**Signature:** `_handle_failure(self, exception: Exception) -> None`  
**Line:** 471  
**Description:** Handle failed call execution.

### `call`

**Signature:** `call(self, operation: Callable) -> Any`  
**Line:** 496  
**Description:** Execute operation through circuit breaker.

Args:
    operation: Function to execute
    *args: Arguments for the operation
    **kwargs: Keyword arguments for the operation
    
Returns:
    Result of the operation
    
Raises:
    Exception: If circuit is open or operation fails

### `get_stats`

**Signature:** `get_stats(self) -> Dict[str, Any]`  
**Line:** 528  
**Description:** Get circuit breaker statistics.

Returns:
    Dictionary containing circuit breaker statistics

### `__init__`

**Signature:** `__init__(self, name: str) -> None`  
**Line:** 559  
**Description:** Initialize fallback strategy.

Args:
    name: Name for identification and logging

### `add_fallback`

**Signature:** `add_fallback(self, operation: Callable, condition: Optional[Callable[[Exception], bool]], priority: int, description: str) -> None`  
**Line:** 579  
**Description:** Add fallback operation.

Args:
    operation: Fallback function to execute
    condition: Optional condition to determine if fallback should be used
    priority: Priority level (lower numbers = higher priority)
    description: Human-readable description of fallback

### `execute_with_fallback`

**Signature:** `execute_with_fallback(self, primary_operation: Callable) -> Dict[str, Any]`  
**Line:** 610  
**Description:** Execute primary operation with fallback support.

Args:
    primary_operation: Primary function to execute
    *args: Arguments for operations
    **kwargs: Keyword arguments for operations
    
Returns:
    Dictionary with execution result and metadata

### `get_stats`

**Signature:** `get_stats(self) -> Dict[str, Any]`  
**Line:** 689  
**Description:** Get fallback execution statistics.

Returns:
    Dictionary containing fallback statistics

### `__init__`

**Signature:** `__init__(self, config: ErrorConfiguration, context: Optional[Context]) -> None`  
**Line:** 726  
**Description:** Initialize recovery orchestrator.

Args:
    config: Error configuration containing recovery settings
    context: Optional Framework0 context for integration

### `_initialize_default_strategies`

**Signature:** `_initialize_default_strategies(self) -> None`  
**Line:** 755  
**Description:** Initialize default recovery strategies from configuration.

### `recover_from_error`

**Signature:** `recover_from_error(self, error_context: ErrorContext, recovery_operation: Callable) -> Dict[str, Any]`  
**Line:** 782  
**Description:** Execute comprehensive recovery for an error.

Args:
    error_context: Error context containing error information
    recovery_operation: Operation to execute for recovery
    *args: Arguments for recovery operation
    **kwargs: Keyword arguments for recovery operation
    
Returns:
    Dictionary containing recovery result and metadata

### `_select_recovery_strategy`

**Signature:** `_select_recovery_strategy(self, error_context: ErrorContext) -> str`  
**Line:** 875  
**Description:** Select appropriate recovery strategy based on error characteristics.

Args:
    error_context: Error context to analyze
    
Returns:
    Name of recommended recovery strategy

### `_execute_retry_recovery`

**Signature:** `_execute_retry_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]`  
**Line:** 898  
**Description:** Execute recovery using retry strategy.

### `_execute_circuit_breaker_recovery`

**Signature:** `_execute_circuit_breaker_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]`  
**Line:** 917  
**Description:** Execute recovery using circuit breaker.

### `_execute_fallback_recovery`

**Signature:** `_execute_fallback_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]`  
**Line:** 943  
**Description:** Execute recovery using fallback strategy.

### `_execute_combined_recovery`

**Signature:** `_execute_combined_recovery(self, error_context: ErrorContext, operation: Callable) -> Dict[str, Any]`  
**Line:** 954  
**Description:** Execute recovery using combined strategies.

### `get_stats`

**Signature:** `get_stats(self) -> Dict[str, Any]`  
**Line:** 995  
**Description:** Get comprehensive recovery statistics.

Returns:
    Dictionary containing all recovery statistics

### `get_logger`

**Signature:** `get_logger(name)`  
**Line:** 32  
**Description:** Fallback logger for standalone usage.

### `protected_operation`

**Signature:** `protected_operation()`  
**Line:** 966  
**Description:** Function: protected_operation


## Classes (7 total)

### `BackoffStrategy`

**Line:** 42  
**Inherits from:** Enum  
**Description:** Available backoff strategies for retry operations.

Each strategy provides different timing patterns for retry attempts:
- FIXED: Fixed delay between attempts
- LINEAR: Linearly increasing delay
- EXPONENTIAL: Exponentially increasing delay
- EXPONENTIAL_JITTER: Exponential with random jitter to prevent thundering herd

### `CircuitState`

**Line:** 58  
**Inherits from:** Enum  
**Description:** Circuit breaker states for service protection.

States follow the classic circuit breaker pattern:
- CLOSED: Normal operation, requests pass through
- OPEN: Circuit is open, requests fail fast
- HALF_OPEN: Testing recovery, limited requests allowed

### `RetryResult`

**Line:** 73  
**Description:** Result of a retry operation with execution metadata.

Contains comprehensive information about retry execution:
- Success status and final result or error
- Execution statistics (attempts, timing, backoff)
- Recovery metadata for analysis and optimization

### `RetryStrategy`

**Line:** 91  
**Description:** Configurable retry logic with backoff patterns and failure handling.

Provides comprehensive retry capabilities:
- Multiple backoff strategies (fixed, linear, exponential, jitter)
- Configurable retry conditions and exception filtering
- Detailed execution tracking and performance analysis
- Integration with Framework0 context and error handling

**Methods (7 total):**
- `__init__`: Initialize retry strategy with configuration.

Args:
    max_attempts: Maximum number of retry attempts
    backoff_strategy: Strategy for calculating retry delays
    initial_delay: Initial delay before first retry (seconds)
    max_delay: Maximum delay between retries (seconds)
    backoff_multiplier: Multiplier for exponential backoff
    jitter_factor: Random jitter factor (0.0-1.0) for jitter strategies
- `add_retry_exception`: Add exception type that should trigger retry.

Args:
    exception_type: Exception class to retry on
- `set_retry_condition`: Set custom retry condition function.

Args:
    condition: Function that takes an exception and returns bool
- `should_retry`: Determine if operation should be retried.

Args:
    exception: Exception that occurred
    attempt: Current attempt number
    
Returns:
    True if should retry, False otherwise
- `calculate_delay`: Calculate delay for retry attempt based on backoff strategy.

Args:
    attempt: Current attempt number (0-based)
    
Returns:
    Delay in seconds before next retry
- `execute_with_retry`: Execute operation with retry logic.

Args:
    operation: Function to execute with retry
    *args: Arguments for the operation
    error_context: Optional error context for Framework0 integration
    **kwargs: Keyword arguments for the operation
    
Returns:
    RetryResult containing execution details and final outcome
- `get_stats`: Get retry execution statistics.

Returns:
    Dictionary containing retry statistics

### `CircuitBreaker`

**Line:** 342  
**Description:** Circuit breaker pattern for service protection and automatic recovery.

Provides service protection through the circuit breaker pattern:
- Automatic failure detection and circuit opening
- Configurable failure thresholds and recovery timeouts
- Half-open testing for recovery detection
- Detailed monitoring and statistics collection

**Methods (11 total):**
- `__init__`: Initialize circuit breaker with configuration.

Args:
    failure_threshold: Number of failures before opening circuit
    recovery_timeout: Time to wait before testing recovery (seconds)
    half_open_max_calls: Maximum calls allowed in half-open state
    name: Name for identification and logging
- `state`: Get current circuit state.
- `is_closed`: Check if circuit is closed (normal operation).
- `is_open`: Check if circuit is open (failing fast).
- `is_half_open`: Check if circuit is half-open (testing recovery).
- `_can_attempt_call`: Check if call can be attempted in current state.

Returns:
    True if call can be attempted, False otherwise
- `_transition_to_half_open`: Transition circuit to half-open state.
- `_handle_success`: Handle successful call execution.
- `_handle_failure`: Handle failed call execution.
- `call`: Execute operation through circuit breaker.

Args:
    operation: Function to execute
    *args: Arguments for the operation
    **kwargs: Keyword arguments for the operation
    
Returns:
    Result of the operation
    
Raises:
    Exception: If circuit is open or operation fails
- `get_stats`: Get circuit breaker statistics.

Returns:
    Dictionary containing circuit breaker statistics

### `FallbackStrategy`

**Line:** 548  
**Description:** Context-aware fallback execution paths with graceful degradation.

Provides fallback capabilities when primary operations fail:
- Multiple fallback levels with prioritization
- Context-aware fallback selection based on error type
- Cached data fallbacks for service degradation scenarios
- Statistical tracking of fallback usage and success rates

**Methods (4 total):**
- `__init__`: Initialize fallback strategy.

Args:
    name: Name for identification and logging
- `add_fallback`: Add fallback operation.

Args:
    operation: Fallback function to execute
    condition: Optional condition to determine if fallback should be used
    priority: Priority level (lower numbers = higher priority)
    description: Human-readable description of fallback
- `execute_with_fallback`: Execute primary operation with fallback support.

Args:
    primary_operation: Primary function to execute
    *args: Arguments for operations
    **kwargs: Keyword arguments for operations
    
Returns:
    Dictionary with execution result and metadata
- `get_stats`: Get fallback execution statistics.

Returns:
    Dictionary containing fallback statistics

### `RecoveryOrchestrator`

**Line:** 715  
**Description:** Coordinate complex recovery workflows with Framework0 integration.

Provides comprehensive recovery orchestration:
- Integration of retry, circuit breaker, and fallback strategies
- Recovery workflow definition and execution
- Framework0 context integration for recipe-level recovery
- Statistical analysis and recovery optimization

**Methods (9 total):**
- `__init__`: Initialize recovery orchestrator.

Args:
    config: Error configuration containing recovery settings
    context: Optional Framework0 context for integration
- `_initialize_default_strategies`: Initialize default recovery strategies from configuration.
- `recover_from_error`: Execute comprehensive recovery for an error.

Args:
    error_context: Error context containing error information
    recovery_operation: Operation to execute for recovery
    *args: Arguments for recovery operation
    **kwargs: Keyword arguments for recovery operation
    
Returns:
    Dictionary containing recovery result and metadata
- `_select_recovery_strategy`: Select appropriate recovery strategy based on error characteristics.

Args:
    error_context: Error context to analyze
    
Returns:
    Name of recommended recovery strategy
- `_execute_retry_recovery`: Execute recovery using retry strategy.
- `_execute_circuit_breaker_recovery`: Execute recovery using circuit breaker.
- `_execute_fallback_recovery`: Execute recovery using fallback strategy.
- `_execute_combined_recovery`: Execute recovery using combined strategies.
- `get_stats`: Get comprehensive recovery statistics.

Returns:
    Dictionary containing all recovery statistics


## Usage Examples

```python
# Import the module
from scriptlets.foundation.errors.recovery_strategies import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `dataclasses`
- `datetime`
- `enum`
- `error_core`
- `logging`
- `orchestrator.context`
- `random`
- `src.core.logger`
- `threading`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
