# error_handlers.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/errors/error_handlers.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T14:43:53.262642  
**File Size:** 36,285 bytes  

## Description
Framework0 Foundation - Error Processing Engine

Error detection, classification, and initial response coordination:
- Proactive error detection from logs and performance metrics
- Automatic error categorization using patterns and ML techniques
- Configurable error routing rules with business logic
- Error deduplication and correlation across recipe executions
- Multi-channel notification system with severity-based escalation

This module handles the "intake" side of error management, processing
errors as they occur and routing them to appropriate recovery systems.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __post_init__**
2. **Function: matches**
3. **Function: __init__**
4. **Function: _load_default_patterns**
5. **Function: add_pattern**
6. **Function: detect_from_log_message**
7. **Function: detect_from_exception**
8. **Function: get_detection_stats**
9. **Function: enable_detection**
10. **Function: disable_detection**
11. **Function: __init__**
12. **Function: classify_error**
13. **Function: _extract_features**
14. **Function: _classify_from_features**
15. **Function: get_classification_stats**
16. **Function: __init__**
17. **Function: _initialize_default_rules**
18. **Function: register_handler**
19. **Function: set_default_handler**
20. **Function: route_error**
21. **Function: _matches_rule**
22. **Function: get_routing_stats**
23. **Function: __init__**
24. **Function: add_error**
25. **Function: _calculate_group_key**
26. **Function: _is_duplicate**
27. **Function: get_error_groups**
28. **Function: get_aggregation_stats**
29. **Function: __init__**
30. **Function: notify_error**
31. **Function: _get_channels_for_severity**
32. **Function: _send_notification**
33. **Function: _format_message**
34. **Function: _send_log_notification**
35. **Function: _send_email_notification**
36. **Function: _send_webhook_notification**
37. **Function: get_notification_stats**
38. **Function: get_logger**
39. **Class: ErrorPattern (2 methods)**
40. **Class: ErrorDetector (8 methods)**
41. **Class: ErrorClassifier (5 methods)**
42. **Class: ErrorRouter (7 methods)**
43. **Class: ErrorAggregator (6 methods)**
44. **Class: ErrorNotifier (9 methods)**

## Functions (38 total)

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 72  
**Description:** Compile regex pattern after initialization.

### `matches`

**Signature:** `matches(self, text: str) -> bool`  
**Line:** 92  
**Description:** Check if pattern matches the given text.

Args:
    text: Text to check for pattern match
    
Returns:
    True if pattern matches, False otherwise

### `__init__`

**Signature:** `__init__(self, config: ErrorConfiguration) -> None`  
**Line:** 119  
**Description:** Initialize error detector with configuration.

Args:
    config: Error configuration containing detection settings

### `_load_default_patterns`

**Signature:** `_load_default_patterns(self) -> None`  
**Line:** 143  
**Description:** Load default error detection patterns.

### `add_pattern`

**Signature:** `add_pattern(self, pattern: ErrorPattern) -> None`  
**Line:** 201  
**Description:** Add custom error detection pattern.

Args:
    pattern: Error pattern to add for detection

### `detect_from_log_message`

**Signature:** `detect_from_log_message(self, log_message: str, log_level: str) -> List[ErrorContext]`  
**Line:** 214  
**Description:** Detect errors from log message content.

Args:
    log_message: Log message to analyze
    log_level: Log level of the message
    
Returns:
    List of detected error contexts

### `detect_from_exception`

**Signature:** `detect_from_exception(self, exception: Exception, context: Optional[Dict[str, Any]]) -> ErrorContext`  
**Line:** 263  
**Description:** Create error context from exception with enhanced detection.

Args:
    exception: Exception that occurred
    context: Optional context information
    
Returns:
    Error context with detection metadata

### `get_detection_stats`

**Signature:** `get_detection_stats(self) -> Dict[str, Any]`  
**Line:** 304  
**Description:** Get error detection statistics.

Returns:
    Dictionary containing detection statistics

### `enable_detection`

**Signature:** `enable_detection(self) -> None`  
**Line:** 314  
**Description:** Enable error detection.

### `disable_detection`

**Signature:** `disable_detection(self) -> None`  
**Line:** 319  
**Description:** Disable error detection.

### `__init__`

**Signature:** `__init__(self, config: ErrorConfiguration) -> None`  
**Line:** 336  
**Description:** Initialize error classifier with configuration.

Args:
    config: Error configuration containing classification settings

### `classify_error`

**Signature:** `classify_error(self, error_context: ErrorContext, override_confidence: Optional[float]) -> ErrorContext`  
**Line:** 358  
**Description:** Classify error and update context with classification metadata.

Args:
    error_context: Error context to classify
    override_confidence: Optional confidence override
    
Returns:
    Error context with updated classification

### `_extract_features`

**Signature:** `_extract_features(self, error_context: ErrorContext) -> Dict[str, Any]`  
**Line:** 402  
**Description:** Extract features from error context for classification.

Args:
    error_context: Error context to analyze
    
Returns:
    Dictionary of extracted features

### `_classify_from_features`

**Signature:** `_classify_from_features(self, features: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 438  
**Description:** Classify error based on extracted features.

Args:
    features: Extracted features for classification
    
Returns:
    Classification result with category, severity, and confidence

### `get_classification_stats`

**Signature:** `get_classification_stats(self) -> Dict[str, Any]`  
**Line:** 490  
**Description:** Get classification statistics.

Returns:
    Dictionary containing classification statistics

### `__init__`

**Signature:** `__init__(self, config: ErrorConfiguration) -> None`  
**Line:** 511  
**Description:** Initialize error router with configuration.

Args:
    config: Error configuration containing routing settings

### `_initialize_default_rules`

**Signature:** `_initialize_default_rules(self) -> None`  
**Line:** 535  
**Description:** Initialize default routing rules.

### `register_handler`

**Signature:** `register_handler(self, name: str, handler: Callable) -> None`  
**Line:** 566  
**Description:** Register error handler for routing.

Args:
    name: Handler name for routing rules
    handler: Callable handler function

### `set_default_handler`

**Signature:** `set_default_handler(self, handler: Callable) -> None`  
**Line:** 577  
**Description:** Set default handler for unrouted errors.

Args:
    handler: Default handler function

### `route_error`

**Signature:** `route_error(self, error_context: ErrorContext) -> Optional[str]`  
**Line:** 587  
**Description:** Route error to appropriate handler.

Args:
    error_context: Error context to route
    
Returns:
    Name of handler that processed the error, or None if no handler

### `_matches_rule`

**Signature:** `_matches_rule(self, error_context: ErrorContext, rule: Dict[str, Any]) -> bool`  
**Line:** 627  
**Description:** Check if error context matches routing rule.

Args:
    error_context: Error context to check
    rule: Routing rule to evaluate
    
Returns:
    True if error matches rule, False otherwise

### `get_routing_stats`

**Signature:** `get_routing_stats(self) -> Dict[str, Any]`  
**Line:** 660  
**Description:** Get routing statistics.

Returns:
    Dictionary containing routing statistics

### `__init__`

**Signature:** `__init__(self, config: ErrorConfiguration) -> None`  
**Line:** 681  
**Description:** Initialize error aggregator with configuration.

Args:
    config: Error configuration containing aggregation settings

### `add_error`

**Signature:** `add_error(self, error_context: ErrorContext) -> str`  
**Line:** 702  
**Description:** Add error to aggregation system.

Args:
    error_context: Error context to aggregate
    
Returns:
    Group ID that the error was assigned to

### `_calculate_group_key`

**Signature:** `_calculate_group_key(self, error_context: ErrorContext) -> str`  
**Line:** 729  
**Description:** Calculate group key for error aggregation.

Args:
    error_context: Error context to group
    
Returns:
    Group key string

### `_is_duplicate`

**Signature:** `_is_duplicate(self, error_context: ErrorContext, group_key: str) -> bool`  
**Line:** 754  
**Description:** Check if error is a duplicate within time window.

Args:
    error_context: Error context to check
    group_key: Group to check for duplicates
    
Returns:
    True if error is a duplicate, False otherwise

### `get_error_groups`

**Signature:** `get_error_groups(self) -> Dict[str, List[ErrorContext]]`  
**Line:** 782  
**Description:** Get current error groups.

Returns:
    Dictionary mapping group keys to error lists

### `get_aggregation_stats`

**Signature:** `get_aggregation_stats(self) -> Dict[str, Any]`  
**Line:** 792  
**Description:** Get aggregation statistics.

Returns:
    Dictionary containing aggregation statistics

### `__init__`

**Signature:** `__init__(self, config: ErrorConfiguration) -> None`  
**Line:** 813  
**Description:** Initialize error notifier with configuration.

Args:
    config: Error configuration containing notification settings

### `notify_error`

**Signature:** `notify_error(self, error_context: ErrorContext, additional_context: Optional[Dict[str, Any]]) -> Dict[str, bool]`  
**Line:** 833  
**Description:** Send error notification through appropriate channels.

Args:
    error_context: Error context to notify about
    additional_context: Optional additional context information
    
Returns:
    Dictionary mapping channel names to success status

### `_get_channels_for_severity`

**Signature:** `_get_channels_for_severity(self, severity: ErrorSeverity, thresholds: Dict[str, str]) -> List[str]`  
**Line:** 873  
**Description:** Get notification channels appropriate for error severity.

Args:
    severity: Error severity level
    thresholds: Severity thresholds for each channel
    
Returns:
    List of channel names to use for notification

### `_send_notification`

**Signature:** `_send_notification(self, channel: str, error_context: ErrorContext, additional_context: Optional[Dict[str, Any]]) -> bool`  
**Line:** 899  
**Description:** Send notification to specific channel.

Args:
    channel: Channel name to send to
    error_context: Error context to notify about
    additional_context: Optional additional context
    
Returns:
    True if notification was sent successfully, False otherwise

### `_format_message`

**Signature:** `_format_message(self, error_context: ErrorContext, additional_context: Optional[Dict[str, Any]]) -> str`  
**Line:** 924  
**Description:** Format error message for notification.

Args:
    error_context: Error context to format
    additional_context: Optional additional context
    
Returns:
    Formatted message string

### `_send_log_notification`

**Signature:** `_send_log_notification(self, message: str, error_context: ErrorContext) -> bool`  
**Line:** 963  
**Description:** Send notification to log.

### `_send_email_notification`

**Signature:** `_send_email_notification(self, message: str, error_context: ErrorContext) -> bool`  
**Line:** 976  
**Description:** Send notification via email (placeholder implementation).

### `_send_webhook_notification`

**Signature:** `_send_webhook_notification(self, message: str, error_context: ErrorContext) -> bool`  
**Line:** 983  
**Description:** Send notification via webhook (placeholder implementation).

### `get_notification_stats`

**Signature:** `get_notification_stats(self) -> Dict[str, Any]`  
**Line:** 990  
**Description:** Get notification statistics.

Returns:
    Dictionary containing notification statistics

### `get_logger`

**Signature:** `get_logger(name)`  
**Line:** 32  
**Description:** Fallback logger for standalone usage.


## Classes (6 total)

### `ErrorPattern`

**Line:** 44  
**Description:** Error detection pattern for automated classification.

Encapsulates pattern matching rules for error identification:
- Regex patterns for log message matching
- Exception type filters for code-based detection
- Severity thresholds for metric-based detection
- Classification rules for automatic categorization

**Methods (2 total):**
- `__post_init__`: Compile regex pattern after initialization.
- `matches`: Check if pattern matches the given text.

Args:
    text: Text to check for pattern match
    
Returns:
    True if pattern matches, False otherwise

### `ErrorDetector`

**Line:** 108  
**Description:** Proactive error detection from multiple sources.

Monitors Framework0 execution for error conditions:
- Log message analysis with pattern matching
- Performance metric threshold monitoring
- Health check integration for predictive detection
- Exception tracking across recipe executions

**Methods (8 total):**
- `__init__`: Initialize error detector with configuration.

Args:
    config: Error configuration containing detection settings
- `_load_default_patterns`: Load default error detection patterns.
- `add_pattern`: Add custom error detection pattern.

Args:
    pattern: Error pattern to add for detection
- `detect_from_log_message`: Detect errors from log message content.

Args:
    log_message: Log message to analyze
    log_level: Log level of the message
    
Returns:
    List of detected error contexts
- `detect_from_exception`: Create error context from exception with enhanced detection.

Args:
    exception: Exception that occurred
    context: Optional context information
    
Returns:
    Error context with detection metadata
- `get_detection_stats`: Get error detection statistics.

Returns:
    Dictionary containing detection statistics
- `enable_detection`: Enable error detection.
- `disable_detection`: Disable error detection.

### `ErrorClassifier`

**Line:** 325  
**Description:** Automatic error categorization using patterns and ML techniques.

Provides intelligent error classification:
- Pattern-based classification with confidence scoring
- Machine learning classification for unknown patterns
- Classification confidence evaluation and validation
- Feedback loop for improving classification accuracy

**Methods (5 total):**
- `__init__`: Initialize error classifier with configuration.

Args:
    config: Error configuration containing classification settings
- `classify_error`: Classify error and update context with classification metadata.

Args:
    error_context: Error context to classify
    override_confidence: Optional confidence override
    
Returns:
    Error context with updated classification
- `_extract_features`: Extract features from error context for classification.

Args:
    error_context: Error context to analyze
    
Returns:
    Dictionary of extracted features
- `_classify_from_features`: Classify error based on extracted features.

Args:
    features: Extracted features for classification
    
Returns:
    Classification result with category, severity, and confidence
- `get_classification_stats`: Get classification statistics.

Returns:
    Dictionary containing classification statistics

### `ErrorRouter`

**Line:** 500  
**Description:** Route errors to appropriate handlers based on type and configuration.

Provides configurable error routing logic:
- Rule-based routing with category and severity filters
- Business logic integration for custom routing decisions
- Load balancing across multiple handler instances
- Fallback routing for unhandled error types

**Methods (7 total):**
- `__init__`: Initialize error router with configuration.

Args:
    config: Error configuration containing routing settings
- `_initialize_default_rules`: Initialize default routing rules.
- `register_handler`: Register error handler for routing.

Args:
    name: Handler name for routing rules
    handler: Callable handler function
- `set_default_handler`: Set default handler for unrouted errors.

Args:
    handler: Default handler function
- `route_error`: Route error to appropriate handler.

Args:
    error_context: Error context to route
    
Returns:
    Name of handler that processed the error, or None if no handler
- `_matches_rule`: Check if error context matches routing rule.

Args:
    error_context: Error context to check
    rule: Routing rule to evaluate
    
Returns:
    True if error matches rule, False otherwise
- `get_routing_stats`: Get routing statistics.

Returns:
    Dictionary containing routing statistics

### `ErrorAggregator`

**Line:** 670  
**Description:** Group related errors for batch processing and deduplication.

Provides error aggregation capabilities:
- Error deduplication based on content similarity
- Time-based error batching for efficiency
- Correlation detection across recipe executions
- Statistical analysis of error patterns

**Methods (6 total):**
- `__init__`: Initialize error aggregator with configuration.

Args:
    config: Error configuration containing aggregation settings
- `add_error`: Add error to aggregation system.

Args:
    error_context: Error context to aggregate
    
Returns:
    Group ID that the error was assigned to
- `_calculate_group_key`: Calculate group key for error aggregation.

Args:
    error_context: Error context to group
    
Returns:
    Group key string
- `_is_duplicate`: Check if error is a duplicate within time window.

Args:
    error_context: Error context to check
    group_key: Group to check for duplicates
    
Returns:
    True if error is a duplicate, False otherwise
- `get_error_groups`: Get current error groups.

Returns:
    Dictionary mapping group keys to error lists
- `get_aggregation_stats`: Get aggregation statistics.

Returns:
    Dictionary containing aggregation statistics

### `ErrorNotifier`

**Line:** 802  
**Description:** Multi-channel error notification system with severity-based escalation.

Provides comprehensive notification capabilities:
- Multiple notification channels (log, email, webhook, Slack)
- Severity-based routing and escalation rules
- Rate limiting and notification batching
- Template-based message formatting

**Methods (9 total):**
- `__init__`: Initialize error notifier with configuration.

Args:
    config: Error configuration containing notification settings
- `notify_error`: Send error notification through appropriate channels.

Args:
    error_context: Error context to notify about
    additional_context: Optional additional context information
    
Returns:
    Dictionary mapping channel names to success status
- `_get_channels_for_severity`: Get notification channels appropriate for error severity.

Args:
    severity: Error severity level
    thresholds: Severity thresholds for each channel
    
Returns:
    List of channel names to use for notification
- `_send_notification`: Send notification to specific channel.

Args:
    channel: Channel name to send to
    error_context: Error context to notify about
    additional_context: Optional additional context
    
Returns:
    True if notification was sent successfully, False otherwise
- `_format_message`: Format error message for notification.

Args:
    error_context: Error context to format
    additional_context: Optional additional context
    
Returns:
    Formatted message string
- `_send_log_notification`: Send notification to log.
- `_send_email_notification`: Send notification via email (placeholder implementation).
- `_send_webhook_notification`: Send notification via webhook (placeholder implementation).
- `get_notification_stats`: Get notification statistics.

Returns:
    Dictionary containing notification statistics


## Usage Examples

```python
# Import the module
from scriptlets.foundation.errors.error_handlers import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `collections`
- `dataclasses`
- `datetime`
- `error_core`
- `hashlib`
- `logging`
- `orchestrator.context`
- `re`
- `src.core.logger`
- `threading`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
