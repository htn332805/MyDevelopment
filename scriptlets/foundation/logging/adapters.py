"""
Framework0 Foundation - Logger Adapters

Context-aware logger adapters for Framework0 integration:
- Framework0LoggerAdapter for automatic context inclusion
- Utility functions for performance and audit logging
- Thread-safe logger management for parallel execution
- Easy-to-use interfaces for other scriptlets
"""

from typing import Dict, Any, Optional, Union
import logging
import uuid
import threading

from orchestrator.context import Context
from .core import create_timestamp


class Framework0LoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that automatically includes Framework0 context information.
    
    Provides seamless integration with Framework0 execution context:
    - Automatic recipe and step information extraction
    - Unique execution ID generation for tracking
    - Thread-safe context management
    - Easy-to-use interface for other scriptlets
    """
    
    def __init__(self, logger: logging.Logger, context: Optional[Context] = None) -> None:
        """
        Initialize the Framework0 logger adapter.
        
        Args:
            logger: The base logger instance to wrap
            context: Framework0 context for extracting contextual information
        """
        super().__init__(logger, {})
        self.context: Optional[Context] = context
        self._execution_id: str = str(uuid.uuid4())[:8]  # Short execution ID
        self._lock: threading.Lock = threading.Lock()    # Thread safety
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """
        Process log message and add Framework0 context information.
        
        Args:
            msg: Log message to process
            kwargs: Additional logging arguments
            
        Returns:
            Tuple of (message, kwargs) with context information added
        """
        with self._lock:  # Ensure thread safety
            # Get or create extra data dictionary
            extra = kwargs.get('extra', {})
            
            # Add execution tracking information
            extra['execution_id'] = self._execution_id
            extra['context_id'] = id(self.context) if self.context else None
            
            # Extract Framework0 context information if available
            if self.context:
                try:
                    # Extract recipe and step information from context
                    extra['recipe_name'] = self.context.get('recipe.name')
                    extra['step_name'] = self.context.get('current_step.name')
                    
                    # Add any additional context data that might be useful
                    extra['recipe_version'] = self.context.get('recipe.version')
                    extra['step_index'] = self.context.get('current_step.index')
                except Exception:
                    # If context extraction fails, continue without it
                    pass
            
            # Update kwargs with enhanced extra information
            kwargs['extra'] = extra
            
        return msg, kwargs
    
    def get_execution_id(self) -> str:
        """
        Get the unique execution ID for this adapter instance.
        
        Returns:
            Unique execution ID string
        """
        return self._execution_id
    
    def update_context(self, new_context: Optional[Context]) -> None:
        """
        Update the Framework0 context for this adapter.
        
        Args:
            new_context: New Framework0 context to use
        """
        with self._lock:
            self.context = new_context


class LoggerManager:
    """
    Thread-safe manager for Framework0 logger instances.
    
    Provides centralized management of logger adapters:
    - Thread-safe logger creation and retrieval
    - Consistent configuration across all loggers
    - Memory-efficient logger reuse
    - Easy cleanup and management
    """
    
    def __init__(self) -> None:
        """
        Initialize the logger manager.
        """
        self._loggers: Dict[str, Framework0LoggerAdapter] = {}
        self._lock: threading.Lock = threading.Lock()
    
    def get_logger(self, name: str, context: Optional[Context] = None) -> Framework0LoggerAdapter:
        """
        Get or create a Framework0 logger adapter.
        
        Args:
            name: Name for the logger (will be prefixed with 'framework0.')
            context: Framework0 context for the logger
            
        Returns:
            Framework0LoggerAdapter instance
        """
        full_name = f"framework0.{name}" if not name.startswith("framework0.") else name
        
        with self._lock:
            if full_name not in self._loggers:
                # Create new logger adapter
                base_logger = logging.getLogger(full_name)
                adapter = Framework0LoggerAdapter(base_logger, context)
                self._loggers[full_name] = adapter
            else:
                # Update context if provided
                if context is not None:
                    self._loggers[full_name].update_context(context)
            
            return self._loggers[full_name]
    
    def update_all_contexts(self, context: Optional[Context]) -> None:
        """
        Update context for all managed loggers.
        
        Args:
            context: New context to apply to all loggers
        """
        with self._lock:
            for adapter in self._loggers.values():
                adapter.update_context(context)
    
    def get_logger_count(self) -> int:
        """
        Get the number of managed loggers.
        
        Returns:
            Number of logger adapters being managed
        """
        with self._lock:
            return len(self._loggers)
    
    def clear_loggers(self) -> None:
        """
        Clear all managed loggers (useful for cleanup).
        """
        with self._lock:
            self._loggers.clear()


def create_logger_utilities(context: Optional[Context] = None) -> Dict[str, Any]:
    """
    Create a complete set of logging utilities for Framework0.
    
    Args:
        context: Optional Framework0 context for initial setup
        
    Returns:
        Dictionary containing all logging utilities and functions
    """
    logger_manager = LoggerManager()
    
    def log_performance_metric(metric_name: str, value: Union[int, float], 
                             unit: str = "", **kwargs) -> None:
        """Log a performance metric in structured format."""
        perf_logger = logger_manager.get_logger("performance", context)
        metric_data = {
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
            "timestamp": create_timestamp(),
            **kwargs
        }
        perf_logger.info(f"Performance: {metric_name} = {value} {unit}",
                        extra={"extra_data": metric_data})
    
    def log_audit_event(event_type: str, details: Dict[str, Any], **kwargs) -> None:
        """Log an audit event for compliance tracking."""
        audit_logger = logger_manager.get_logger("audit", context)
        audit_data = {
            "event_type": event_type,
            "details": details,
            "timestamp": create_timestamp(),
            **kwargs
        }
        audit_logger.info(f"Audit: {event_type}", extra={"extra_data": audit_data})
    
    def log_error_with_context(error: Exception, operation: str, **kwargs) -> None:
        """Log an error with full context information."""
        error_logger = logger_manager.get_logger("errors", context)
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "operation": operation,
            "timestamp": create_timestamp(),
            **kwargs
        }
        error_logger.error(f"Error in {operation}: {error}", 
                          exc_info=True, extra={"extra_data": error_data})
    
    return {
        "logger_manager": logger_manager,
        "get_logger": lambda name, ctx=context: logger_manager.get_logger(name, ctx),
        "log_performance": log_performance_metric,
        "log_audit": log_audit_event,
        "log_error": log_error_with_context
    }