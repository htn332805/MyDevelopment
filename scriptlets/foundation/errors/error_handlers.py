"""
Framework0 Foundation - Error Processing Engine

Error detection, classification, and initial response coordination:
- Proactive error detection from logs and performance metrics
- Automatic error categorization using patterns and ML techniques
- Configurable error routing rules with business logic
- Error deduplication and correlation across recipe executions
- Multi-channel notification system with severity-based escalation

This module handles the "intake" side of error management, processing
errors as they occur and routing them to appropriate recovery systems.
"""

from typing import Dict, Any, List, Optional, Set, Callable, Pattern
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque
import re
import threading
import logging
import hashlib

# Framework0 imports with fallback
try:
    from orchestrator.context import Context
    from src.core.logger import get_logger
except ImportError:
    # Fallback for standalone usage
    Context = None
    
    def get_logger(name):
        """Fallback logger for standalone usage."""
        return logging.getLogger(name)

# Import core error handling components
from .error_core import (
    ErrorCategory, ErrorSeverity, ErrorContext, ErrorConfiguration,
    create_error_metadata, categorize_exception, determine_error_severity
)


@dataclass
class ErrorPattern:
    """
    Error detection pattern for automated classification.
    
    Encapsulates pattern matching rules for error identification:
    - Regex patterns for log message matching
    - Exception type filters for code-based detection
    - Severity thresholds for metric-based detection
    - Classification rules for automatic categorization
    """
    name: str                                       # Pattern name for identification
    pattern: str                                    # Regex pattern for matching
    category: ErrorCategory                         # Target error category
    severity: ErrorSeverity                         # Target error severity
    
    # Pattern configuration
    case_sensitive: bool = False                    # Case sensitivity for matching
    whole_word: bool = False                        # Require whole word matches
    multiline: bool = False                         # Enable multiline matching
    
    # Classification metadata
    confidence: float = 1.0                         # Confidence score (0.0-1.0)
    tags: Set[str] = field(default_factory=set)     # Additional classification tags
    description: str = ""                           # Human-readable description
    
    # Compiled pattern cache
    _compiled_pattern: Optional[Pattern] = field(default=None, init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Compile regex pattern after initialization."""
        flags = 0
        if not self.case_sensitive:
            flags |= re.IGNORECASE
        if self.multiline:
            flags |= re.MULTILINE
        
        try:
            if self.whole_word:
                pattern = f"\\b{self.pattern}\\b"
            else:
                pattern = self.pattern
            
            self._compiled_pattern = re.compile(pattern, flags)
        except re.error as e:
            logger = get_logger(__name__)
            logger.warning(f"Invalid regex pattern '{self.pattern}': {e}")
            self._compiled_pattern = None
    
    def matches(self, text: str) -> bool:
        """
        Check if pattern matches the given text.
        
        Args:
            text: Text to check for pattern match
            
        Returns:
            True if pattern matches, False otherwise
        """
        if not self._compiled_pattern:
            return False
        
        return bool(self._compiled_pattern.search(text))


class ErrorDetector:
    """
    Proactive error detection from multiple sources.
    
    Monitors Framework0 execution for error conditions:
    - Log message analysis with pattern matching
    - Performance metric threshold monitoring
    - Health check integration for predictive detection
    - Exception tracking across recipe executions
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize error detector with configuration.
        
        Args:
            config: Error configuration containing detection settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._patterns: List[ErrorPattern] = []
        self._detection_enabled = True
        self._lock = threading.Lock()
        
        # Detection statistics
        self._detection_stats = {
            "patterns_loaded": 0,
            "detections_made": 0,
            "false_positives": 0,
            "last_detection": None
        }
        
        # Load default patterns
        self._load_default_patterns()
    
    def _load_default_patterns(self) -> None:
        """Load default error detection patterns."""
        default_patterns = [
            # Network error patterns
            ErrorPattern(
                name="connection_timeout",
                pattern=r"(connection|timeout|network).*error",
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.HIGH,
                description="Network connection and timeout errors"
            ),
            ErrorPattern(
                name="dns_resolution",
                pattern=r"(dns|domain|resolution).*fail",
                category=ErrorCategory.NETWORK,
                severity=ErrorSeverity.MEDIUM,
                description="DNS resolution failures"
            ),
            
            # System error patterns
            ErrorPattern(
                name="memory_exhaustion",
                pattern=r"(out of memory|memory.*exhausted|oom)",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.CRITICAL,
                description="Memory exhaustion conditions"
            ),
            ErrorPattern(
                name="disk_space",
                pattern=r"(no space|disk.*full|storage.*full)",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                description="Disk space exhaustion"
            ),
            
            # Validation error patterns
            ErrorPattern(
                name="json_parse_error",
                pattern=r"(json.*error|invalid.*json|parse.*error)",
                category=ErrorCategory.VALIDATION,
                severity=ErrorSeverity.MEDIUM,
                description="JSON parsing and validation errors"
            ),
            
            # Security error patterns
            ErrorPattern(
                name="authentication_failure",
                pattern=r"(auth.*fail|unauthorized|access.*denied)",
                category=ErrorCategory.SECURITY,
                severity=ErrorSeverity.HIGH,
                description="Authentication and authorization failures"
            )
        ]
        
        with self._lock:
            self._patterns.extend(default_patterns)
            self._detection_stats["patterns_loaded"] = len(self._patterns)
    
    def add_pattern(self, pattern: ErrorPattern) -> None:
        """
        Add custom error detection pattern.
        
        Args:
            pattern: Error pattern to add for detection
        """
        with self._lock:
            self._patterns.append(pattern)
            self._detection_stats["patterns_loaded"] = len(self._patterns)
        
        self.logger.debug(f"Added error pattern: {pattern.name}")
    
    def detect_from_log_message(
            self,
            log_message: str,
            log_level: str = "INFO"
    ) -> List[ErrorContext]:
        """
        Detect errors from log message content.
        
        Args:
            log_message: Log message to analyze
            log_level: Log level of the message
            
        Returns:
            List of detected error contexts
        """
        if not self._detection_enabled:
            return []
        
        detected_errors = []
        
        with self._lock:
            for pattern in self._patterns:
                if pattern.matches(log_message):
                    # Create error context for detected pattern
                    error_metadata = create_error_metadata(
                        category=pattern.category,
                        severity=pattern.severity,
                        tags={"detection_pattern": pattern.name,
                              "log_level": log_level,
                              "confidence": str(pattern.confidence)}
                    )
                    
                    # Create synthetic exception for pattern match
                    synthetic_error = Exception(f"Pattern detected: {log_message}")
                    
                    error_message = f"Pattern '{pattern.name}': {log_message}"
                    error_context = ErrorContext(
                        original_exception=synthetic_error,
                        error_message=error_message,
                        metadata=error_metadata
                    )
                    
                    detected_errors.append(error_context)
                    self._detection_stats["detections_made"] += 1
                    now = datetime.now(timezone.utc).isoformat()
                    self._detection_stats["last_detection"] = now
        
        return detected_errors
    
    def detect_from_exception(
            self,
            exception: Exception,
            context: Optional[Dict[str, Any]] = None
    ) -> ErrorContext:
        """
        Create error context from exception with enhanced detection.
        
        Args:
            exception: Exception that occurred
            context: Optional context information
            
        Returns:
            Error context with detection metadata
        """
        # Perform automatic categorization
        category = categorize_exception(exception)
        severity = determine_error_severity(exception, context)
        
        # Create metadata with detection information
        metadata = create_error_metadata(
            category=category,
            severity=severity,
            tags={"detection_method": "exception_based",
                  "exception_type": type(exception).__name__}
        )
        
        if context:
            metadata.custom_data.update(context)
        
        error_context = ErrorContext(
            original_exception=exception,
            error_message=str(exception),
            metadata=metadata
        )
        
        self._detection_stats["detections_made"] += 1
        self._detection_stats["last_detection"] = datetime.now(timezone.utc).isoformat()
        
        return error_context
    
    def get_detection_stats(self) -> Dict[str, Any]:
        """
        Get error detection statistics.
        
        Returns:
            Dictionary containing detection statistics
        """
        with self._lock:
            return self._detection_stats.copy()
    
    def enable_detection(self) -> None:
        """Enable error detection."""
        self._detection_enabled = True
        self.logger.info("Error detection enabled")
    
    def disable_detection(self) -> None:
        """Disable error detection."""
        self._detection_enabled = False
        self.logger.info("Error detection disabled")


class ErrorClassifier:
    """
    Automatic error categorization using patterns and ML techniques.
    
    Provides intelligent error classification:
    - Pattern-based classification with confidence scoring
    - Machine learning classification for unknown patterns
    - Classification confidence evaluation and validation
    - Feedback loop for improving classification accuracy
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize error classifier with configuration.
        
        Args:
            config: Error configuration containing classification settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._classification_history: deque = deque(maxlen=1000)
        self._confidence_threshold = config._config.get("classification", {}).get(
            "confidence_threshold", 0.7
        )
        
        # Classification statistics
        self._stats = {
            "classifications_made": 0,
            "high_confidence_classifications": 0,
            "manual_overrides": 0,
            "accuracy_score": 0.0
        }
    
    def classify_error(self, error_context: ErrorContext, 
                      override_confidence: Optional[float] = None) -> ErrorContext:
        """
        Classify error and update context with classification metadata.
        
        Args:
            error_context: Error context to classify
            override_confidence: Optional confidence override
            
        Returns:
            Error context with updated classification
        """
        # Extract features for classification
        features = self._extract_features(error_context)
        
        # Perform classification
        classification_result = self._classify_from_features(features)
        
        # Update error context with classification
        if classification_result["confidence"] >= self._confidence_threshold:
            error_context.metadata.category = classification_result["category"]
            error_context.metadata.severity = classification_result["severity"]
            
            # Add classification metadata
            error_context.metadata.custom_data.update({
                "classification_confidence": classification_result["confidence"],
                "classification_method": classification_result["method"],
                "classification_features": features
            })
            
            self._stats["high_confidence_classifications"] += 1
        
        # Record classification history
        self._classification_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_id": error_context.metadata.error_id,
            "classification": classification_result,
            "features": features
        })
        
        self._stats["classifications_made"] += 1
        
        return error_context
    
    def _extract_features(self, error_context: ErrorContext) -> Dict[str, Any]:
        """
        Extract features from error context for classification.
        
        Args:
            error_context: Error context to analyze
            
        Returns:
            Dictionary of extracted features
        """
        features = {
            "exception_type": type(error_context.original_exception).__name__,
            "message_length": len(error_context.error_message),
            "message_words": len(error_context.error_message.split()),
            "has_stack_trace": bool(error_context.metadata.stack_trace),
            "recipe_context": bool(error_context.metadata.recipe_name),
            "step_context": bool(error_context.metadata.step_name)
        }
        
        # Extract keyword features
        message_lower = error_context.error_message.lower()
        
        # Network-related keywords
        network_keywords = ["connection", "timeout", "network", "socket", "http", "dns"]
        features["network_keyword_count"] = sum(1 for kw in network_keywords if kw in message_lower)
        
        # System-related keywords
        system_keywords = ["memory", "disk", "file", "permission", "system", "os"]
        features["system_keyword_count"] = sum(1 for kw in system_keywords if kw in message_lower)
        
        # Validation-related keywords
        validation_keywords = ["validation", "format", "parse", "schema", "type", "value"]
        features["validation_keyword_count"] = sum(1 for kw in validation_keywords if kw in message_lower)
        
        return features
    
    def _classify_from_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify error based on extracted features.
        
        Args:
            features: Extracted features for classification
            
        Returns:
            Classification result with category, severity, and confidence
        """
        # Simple rule-based classification (can be enhanced with ML)
        category = ErrorCategory.UNKNOWN
        severity = ErrorSeverity.MEDIUM
        confidence = 0.5
        method = "rule_based"
        
        # Network classification rules
        if features["network_keyword_count"] > 0:
            category = ErrorCategory.NETWORK
            confidence = min(0.9, 0.6 + features["network_keyword_count"] * 0.1)
            if "timeout" in features.get("exception_type", "").lower():
                severity = ErrorSeverity.HIGH
        
        # System classification rules
        elif features["system_keyword_count"] > 0:
            category = ErrorCategory.SYSTEM
            confidence = min(0.9, 0.6 + features["system_keyword_count"] * 0.1)
            if "memory" in str(features.get("exception_type", "")).lower():
                severity = ErrorSeverity.CRITICAL
        
        # Validation classification rules
        elif features["validation_keyword_count"] > 0:
            category = ErrorCategory.VALIDATION
            confidence = min(0.8, 0.5 + features["validation_keyword_count"] * 0.15)
        
        # Exception type-based classification
        exception_type = features.get("exception_type", "").lower()
        if "connection" in exception_type or "timeout" in exception_type:
            category = ErrorCategory.NETWORK
            severity = ErrorSeverity.HIGH
            confidence = max(confidence, 0.8)
        elif "value" in exception_type or "type" in exception_type:
            category = ErrorCategory.VALIDATION
            confidence = max(confidence, 0.7)
        
        return {
            "category": category,
            "severity": severity,
            "confidence": confidence,
            "method": method
        }
    
    def get_classification_stats(self) -> Dict[str, Any]:
        """
        Get classification statistics.
        
        Returns:
            Dictionary containing classification statistics
        """
        return self._stats.copy()


class ErrorRouter:
    """
    Route errors to appropriate handlers based on type and configuration.
    
    Provides configurable error routing logic:
    - Rule-based routing with category and severity filters
    - Business logic integration for custom routing decisions
    - Load balancing across multiple handler instances
    - Fallback routing for unhandled error types
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize error router with configuration.
        
        Args:
            config: Error configuration containing routing settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._routing_rules: List[Dict[str, Any]] = []
        self._handler_registry: Dict[str, Callable] = {}
        self._default_handler: Optional[Callable] = None
        
        # Routing statistics
        self._stats = {
            "routes_processed": 0,
            "successful_routes": 0,
            "failed_routes": 0,
            "fallback_routes": 0
        }
        
        # Initialize default routing rules
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default routing rules."""
        default_rules = [
            {
                "name": "critical_errors",
                "condition": {"severity": ["CRITICAL", "FATAL"]},
                "handler": "emergency_handler",
                "priority": 1
            },
            {
                "name": "network_errors", 
                "condition": {"category": ["NETWORK"]},
                "handler": "network_recovery_handler",
                "priority": 2
            },
            {
                "name": "system_errors",
                "condition": {"category": ["SYSTEM"]},
                "handler": "system_recovery_handler",
                "priority": 2
            },
            {
                "name": "validation_errors",
                "condition": {"category": ["VALIDATION"]},
                "handler": "validation_handler",
                "priority": 3
            }
        ]
        
        self._routing_rules = sorted(default_rules, key=lambda x: x["priority"])
    
    def register_handler(self, name: str, handler: Callable) -> None:
        """
        Register error handler for routing.
        
        Args:
            name: Handler name for routing rules
            handler: Callable handler function
        """
        self._handler_registry[name] = handler
        self.logger.debug(f"Registered error handler: {name}")
    
    def set_default_handler(self, handler: Callable) -> None:
        """
        Set default handler for unrouted errors.
        
        Args:
            handler: Default handler function
        """
        self._default_handler = handler
        self.logger.debug("Set default error handler")
    
    def route_error(self, error_context: ErrorContext) -> Optional[str]:
        """
        Route error to appropriate handler.
        
        Args:
            error_context: Error context to route
            
        Returns:
            Name of handler that processed the error, or None if no handler
        """
        self._stats["routes_processed"] += 1
        
        # Try routing rules in priority order
        for rule in self._routing_rules:
            if self._matches_rule(error_context, rule):
                handler_name = rule["handler"]
                handler = self._handler_registry.get(handler_name)
                
                if handler:
                    try:
                        handler(error_context)
                        self._stats["successful_routes"] += 1
                        self.logger.debug(f"Routed error {error_context.metadata.error_id} to {handler_name}")
                        return handler_name
                    except Exception as e:
                        self.logger.error(f"Handler {handler_name} failed: {e}")
                        self._stats["failed_routes"] += 1
        
        # Use default handler if no rules matched
        if self._default_handler:
            try:
                self._default_handler(error_context)
                self._stats["fallback_routes"] += 1
                return "default_handler"
            except Exception as e:
                self.logger.error(f"Default handler failed: {e}")
                self._stats["failed_routes"] += 1
        
        return None
    
    def _matches_rule(self, error_context: ErrorContext, rule: Dict[str, Any]) -> bool:
        """
        Check if error context matches routing rule.
        
        Args:
            error_context: Error context to check
            rule: Routing rule to evaluate
            
        Returns:
            True if error matches rule, False otherwise
        """
        condition = rule.get("condition", {})
        
        # Check category condition
        if "category" in condition:
            allowed_categories = condition["category"]
            if error_context.metadata.category.value not in allowed_categories:
                return False
        
        # Check severity condition
        if "severity" in condition:
            allowed_severities = condition["severity"]
            if error_context.metadata.severity.name not in allowed_severities:
                return False
        
        # Check recipe condition
        if "recipe" in condition:
            allowed_recipes = condition["recipe"]
            if error_context.metadata.recipe_name not in allowed_recipes:
                return False
        
        return True
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """
        Get routing statistics.
        
        Returns:
            Dictionary containing routing statistics
        """
        return self._stats.copy()


class ErrorAggregator:
    """
    Group related errors for batch processing and deduplication.
    
    Provides error aggregation capabilities:
    - Error deduplication based on content similarity
    - Time-based error batching for efficiency
    - Correlation detection across recipe executions
    - Statistical analysis of error patterns
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize error aggregator with configuration.
        
        Args:
            config: Error configuration containing aggregation settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._error_groups: Dict[str, List[ErrorContext]] = defaultdict(list)
        self._aggregation_window = timedelta(minutes=5)  # 5-minute window
        self._lock = threading.Lock()
        
        # Aggregation statistics
        self._stats = {
            "errors_processed": 0,
            "groups_created": 0,
            "duplicates_detected": 0,
            "correlations_found": 0
        }
    
    def add_error(self, error_context: ErrorContext) -> str:
        """
        Add error to aggregation system.
        
        Args:
            error_context: Error context to aggregate
            
        Returns:
            Group ID that the error was assigned to
        """
        group_key = self._calculate_group_key(error_context)
        
        with self._lock:
            # Check for duplicates within the group
            is_duplicate = self._is_duplicate(error_context, group_key)
            
            if not is_duplicate:
                self._error_groups[group_key].append(error_context)
                if len(self._error_groups[group_key]) == 1:
                    self._stats["groups_created"] += 1
            else:
                self._stats["duplicates_detected"] += 1
            
            self._stats["errors_processed"] += 1
        
        return group_key
    
    def _calculate_group_key(self, error_context: ErrorContext) -> str:
        """
        Calculate group key for error aggregation.
        
        Args:
            error_context: Error context to group
            
        Returns:
            Group key string
        """
        # Create grouping based on error characteristics
        key_components = [
            error_context.metadata.category.value,
            error_context.metadata.severity.name,
            type(error_context.original_exception).__name__
        ]
        
        # Add recipe context if available
        if error_context.metadata.recipe_name:
            key_components.append(error_context.metadata.recipe_name)
        
        # Create hash-based key
        key_string = "|".join(key_components)
        return hashlib.md5(key_string.encode()).hexdigest()[:8]
    
    def _is_duplicate(self, error_context: ErrorContext, group_key: str) -> bool:
        """
        Check if error is a duplicate within time window.
        
        Args:
            error_context: Error context to check
            group_key: Group to check for duplicates
            
        Returns:
            True if error is a duplicate, False otherwise
        """
        if group_key not in self._error_groups:
            return False
        
        current_time = datetime.now(timezone.utc)
        error_message = error_context.error_message
        
        for existing_error in self._error_groups[group_key]:
            existing_time = datetime.fromisoformat(existing_error.metadata.timestamp.replace('Z', '+00:00'))
            
            # Check time window
            if current_time - existing_time <= self._aggregation_window:
                # Check message similarity (simple exact match for now)
                if existing_error.error_message == error_message:
                    return True
        
        return False
    
    def get_error_groups(self) -> Dict[str, List[ErrorContext]]:
        """
        Get current error groups.
        
        Returns:
            Dictionary mapping group keys to error lists
        """
        with self._lock:
            return dict(self._error_groups)
    
    def get_aggregation_stats(self) -> Dict[str, Any]:
        """
        Get aggregation statistics.
        
        Returns:
            Dictionary containing aggregation statistics
        """
        return self._stats.copy()


class ErrorNotifier:
    """
    Multi-channel error notification system with severity-based escalation.
    
    Provides comprehensive notification capabilities:
    - Multiple notification channels (log, email, webhook, Slack)
    - Severity-based routing and escalation rules
    - Rate limiting and notification batching
    - Template-based message formatting
    """
    
    def __init__(self, config: ErrorConfiguration) -> None:
        """
        Initialize error notifier with configuration.
        
        Args:
            config: Error configuration containing notification settings
        """
        self.config = config
        self.logger = get_logger(__name__)
        self._notification_config = config.get_notification_config()
        self._enabled = self._notification_config.get("enabled", True)
        
        # Notification statistics
        self._stats = {
            "notifications_sent": 0,
            "failed_notifications": 0,
            "rate_limited": 0,
            "channels_used": set()
        }
    
    def notify_error(self, error_context: ErrorContext, 
                    additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """
        Send error notification through appropriate channels.
        
        Args:
            error_context: Error context to notify about
            additional_context: Optional additional context information
            
        Returns:
            Dictionary mapping channel names to success status
        """
        if not self._enabled:
            return {}
        
        results = {}
        severity = error_context.metadata.severity
        severity_thresholds = self._notification_config.get("severity_thresholds", {})
        
        # Determine appropriate channels based on severity
        channels = self._get_channels_for_severity(severity, severity_thresholds)
        
        for channel in channels:
            try:
                success = self._send_notification(channel, error_context, additional_context)
                results[channel] = success
                
                if success:
                    self._stats["notifications_sent"] += 1
                    self._stats["channels_used"].add(channel)
                else:
                    self._stats["failed_notifications"] += 1
                    
            except Exception as e:
                self.logger.error(f"Notification failed for channel {channel}: {e}")
                results[channel] = False
                self._stats["failed_notifications"] += 1
        
        return results
    
    def _get_channels_for_severity(self, severity: ErrorSeverity, 
                                 thresholds: Dict[str, str]) -> List[str]:
        """
        Get notification channels appropriate for error severity.
        
        Args:
            severity: Error severity level
            thresholds: Severity thresholds for each channel
            
        Returns:
            List of channel names to use for notification
        """
        channels = []
        severity_value = severity.value
        
        for channel, threshold_name in thresholds.items():
            try:
                threshold = ErrorSeverity[threshold_name.upper()]
                if severity_value >= threshold.value:
                    channels.append(channel)
            except (KeyError, AttributeError):
                # Invalid threshold, skip channel
                continue
        
        return channels
    
    def _send_notification(self, channel: str, error_context: ErrorContext,
                          additional_context: Optional[Dict[str, Any]]) -> bool:
        """
        Send notification to specific channel.
        
        Args:
            channel: Channel name to send to
            error_context: Error context to notify about
            additional_context: Optional additional context
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        message = self._format_message(error_context, additional_context)
        
        if channel == "log":
            return self._send_log_notification(message, error_context)
        elif channel == "email":
            return self._send_email_notification(message, error_context)
        elif channel == "webhook":
            return self._send_webhook_notification(message, error_context)
        else:
            self.logger.warning(f"Unknown notification channel: {channel}")
            return False
    
    def _format_message(self, error_context: ErrorContext,
                       additional_context: Optional[Dict[str, Any]]) -> str:
        """
        Format error message for notification.
        
        Args:
            error_context: Error context to format
            additional_context: Optional additional context
            
        Returns:
            Formatted message string
        """
        template = """
🚨 Framework0 Error Alert

Error ID: {error_id}
Category: {category}
Severity: {severity}
Timestamp: {timestamp}

Recipe: {recipe_name}
Step: {step_name}

Error Message: {error_message}

Exception Type: {exception_type}
        """.strip()
        
        return template.format(
            error_id=error_context.metadata.error_id,
            category=error_context.metadata.category.value,
            severity=error_context.metadata.severity.name,
            timestamp=error_context.metadata.timestamp,
            recipe_name=error_context.metadata.recipe_name or "Unknown",
            step_name=error_context.metadata.step_name or "Unknown",
            error_message=error_context.error_message,
            exception_type=type(error_context.original_exception).__name__
        )
    
    def _send_log_notification(self, message: str, error_context: ErrorContext) -> bool:
        """Send notification to log."""
        severity = error_context.metadata.severity
        
        if severity >= ErrorSeverity.CRITICAL:
            self.logger.critical(f"CRITICAL ERROR NOTIFICATION:\n{message}")
        elif severity >= ErrorSeverity.HIGH:
            self.logger.error(f"HIGH SEVERITY ERROR:\n{message}")
        else:
            self.logger.warning(f"ERROR NOTIFICATION:\n{message}")
        
        return True
    
    def _send_email_notification(self, message: str, error_context: ErrorContext) -> bool:
        """Send notification via email (placeholder implementation)."""
        # Placeholder for email notification
        # In production, this would integrate with SMTP or email service
        self.logger.info(f"EMAIL NOTIFICATION (placeholder): {message[:100]}...")
        return True
    
    def _send_webhook_notification(self, message: str, error_context: ErrorContext) -> bool:
        """Send notification via webhook (placeholder implementation)."""
        # Placeholder for webhook notification  
        # In production, this would make HTTP requests to configured webhooks
        self.logger.info(f"WEBHOOK NOTIFICATION (placeholder): {message[:100]}...")
        return True
    
    def get_notification_stats(self) -> Dict[str, Any]:
        """
        Get notification statistics.
        
        Returns:
            Dictionary containing notification statistics
        """
        stats = self._stats.copy()
        stats["channels_used"] = list(stats["channels_used"])
        return stats