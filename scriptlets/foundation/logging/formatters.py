"""
Framework0 Foundation - Logging Formatters

Specialized formatters for different output formats and targets:
- ContextAwareFormatter for Framework0 integration
- JSON structured formatter for machine parsing
- Human-readable formatters for development and operations
- Error and exception formatting with stack traces
"""

from typing import Dict, Any, Optional
import logging
import json
import threading
import os
import traceback
from dataclasses import asdict

from .core import LogEntry, LogFormat, create_timestamp


class ContextAwareFormatter(logging.Formatter):
    """
    Custom formatter that includes Framework0 context in log entries.
    
    Automatically extracts and includes contextual information:
    - Recipe and step execution context
    - Thread and process identification for parallel execution
    - Execution tracking for distributed operations
    - Custom extra data for specialized logging needs
    """
    
    def __init__(self, format_type: LogFormat, include_context: bool = True) -> None:
        """
        Initialize the context-aware formatter.
        
        Args:
            format_type: The type of formatting to apply (JSON, text, etc.)
            include_context: Whether to include Framework0 context information
        """
        super().__init__()
        self.format_type: LogFormat = format_type
        self.include_context: bool = include_context
        
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with Framework0 context information.
        
        Args:
            record: The log record to format
            
        Returns:
            Formatted log message string
        """
        try:
            # Create structured log entry from record
            log_entry = self._create_log_entry_from_record(record)
            
            # Format according to specified type
            if self.format_type == LogFormat.STRUCTURED_JSON:
                return self._format_as_json(log_entry)
            elif self.format_type == LogFormat.DETAILED_TEXT:
                return self._format_as_detailed_text(log_entry)
            else:
                return self._format_as_simple_text(log_entry)
                
        except Exception as formatting_error:
            # Fallback formatting if custom formatting fails
            return self._create_fallback_format(record, formatting_error)
    
    def _create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry:
        """
        Create structured LogEntry from logging.LogRecord.
        
        Args:
            record: Standard logging record
            
        Returns:
            Structured LogEntry with Framework0 context
        """
        # Extract Framework0 context information from record extras
        context_id = getattr(record, 'context_id', None)
        recipe_name = getattr(record, 'recipe_name', None) 
        step_name = getattr(record, 'step_name', None)
        execution_id = getattr(record, 'execution_id', None)
        extra_data = getattr(record, 'extra_data', None)
        
        # Create log entry with all available information
        log_entry = LogEntry(
            timestamp=create_timestamp(),
            level=record.levelname,
            logger_name=record.name,
            message=record.getMessage(),
            context_id=str(context_id) if context_id else None,
            recipe_name=recipe_name,
            step_name=step_name,
            execution_id=execution_id,
            thread_id=str(threading.get_ident()),
            process_id=os.getpid(),
            extra_data=extra_data
        )
        
        # Add stack trace for error conditions
        if record.levelno >= logging.ERROR and record.exc_info:
            log_entry.stack_trace = "".join(
                traceback.format_exception(*record.exc_info)
            )
        
        return log_entry
    
    def _format_as_json(self, entry: LogEntry) -> str:
        """
        Format log entry as structured JSON.
        
        Args:
            entry: Structured log entry
            
        Returns:
            JSON formatted string
        """
        # Convert dataclass to dictionary and serialize as JSON
        entry_dict = asdict(entry)
        
        # Remove None values for cleaner JSON
        entry_dict = {k: v for k, v in entry_dict.items() if v is not None}
        
        return json.dumps(entry_dict, default=str, ensure_ascii=False)
    
    def _format_as_simple_text(self, entry: LogEntry) -> str:
        """
        Format log entry as simple readable text.
        
        Args:
            entry: Structured log entry
            
        Returns:
            Simple text formatted string
        """
        return (f"{entry.timestamp} [{entry.level:8}] "
                f"{entry.logger_name}: {entry.message}")
    
    def _format_as_detailed_text(self, entry: LogEntry) -> str:
        """
        Format log entry with detailed context information.
        
        Args:
            entry: Structured log entry
            
        Returns:
            Detailed text formatted string with context
        """
        # Build header with system and execution information
        header_parts = [
            f"{entry.timestamp} [{entry.level:8}] {entry.logger_name}",
            f"PID:{entry.process_id} TID:{entry.thread_id}"
        ]
        
        # Add Framework0 context if available
        if entry.recipe_name:
            header_parts.append(f"Recipe:{entry.recipe_name}")
        if entry.step_name:
            header_parts.append(f"Step:{entry.step_name}")
        if entry.execution_id:
            # Truncate execution ID for readability
            short_exec_id = entry.execution_id[:8] if entry.execution_id else ""
            header_parts.append(f"Exec:{short_exec_id}")
        
        # Combine header components
        header = " | ".join(header_parts)
        
        # Format main message
        message_line = f"  → {entry.message}"
        
        # Combine header and message
        result = f"{header}\n{message_line}"
        
        # Add extra data if present
        if entry.extra_data:
            extra_json = json.dumps(entry.extra_data, default=str, indent=2)
            result += f"\n  Extra: {extra_json}"
        
        # Add stack trace if present
        if entry.stack_trace:
            result += f"\n  Stack: {entry.stack_trace}"
        
        return result
    
    def _create_fallback_format(self, record: logging.LogRecord, 
                              error: Exception) -> str:
        """
        Create fallback format when normal formatting fails.
        
        Args:
            record: Original log record
            error: Formatting error that occurred
            
        Returns:
            Basic formatted string with error information
        """
        timestamp = create_timestamp()
        return (f"[LOGGING ERROR] {timestamp} - {record.getMessage()} "
                f"(Format Error: {error})")


class AuditFormatter(ContextAwareFormatter):
    """
    Specialized formatter for audit logging with compliance focus.
    
    Always uses structured JSON format for compliance and security analysis.
    Includes additional audit-specific fields and ensures all required
    information is captured for regulatory and security requirements.
    """
    
    def __init__(self) -> None:
        """Initialize audit formatter with JSON format."""
        super().__init__(LogFormat.STRUCTURED_JSON, include_context=True)
    
    def _create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry:
        """
        Create audit log entry with additional compliance fields.
        
        Args:
            record: Standard logging record
            
        Returns:
            LogEntry enhanced for audit purposes
        """
        # Get base log entry
        entry = super()._create_log_entry_from_record(record)
        
        # Add audit-specific extra data
        if not entry.extra_data:
            entry.extra_data = {}
        
        # Add audit metadata
        entry.extra_data.update({
            "audit_category": getattr(record, 'audit_category', 'general'),
            "compliance_level": getattr(record, 'compliance_level', 'standard'),
            "audit_source": record.name
        })
        
        return entry


class PerformanceFormatter(ContextAwareFormatter):
    """
    Specialized formatter for performance and metrics logging.
    
    Optimized for performance data analysis and monitoring systems.
    Includes timing information and resource utilization data.
    """
    
    def __init__(self) -> None:
        """Initialize performance formatter with JSON format."""
        super().__init__(LogFormat.STRUCTURED_JSON, include_context=True)
    
    def _create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry:
        """
        Create performance log entry with metrics data.
        
        Args:
            record: Standard logging record
            
        Returns:
            LogEntry enhanced for performance analysis
        """
        # Get base log entry
        entry = super()._create_log_entry_from_record(record)
        
        # Add performance-specific extra data
        if not entry.extra_data:
            entry.extra_data = {}
        
        # Add performance metadata
        entry.extra_data.update({
            "performance_category": getattr(record, 'performance_category', 'timing'),
            "measurement_unit": getattr(record, 'measurement_unit', ''),
            "measurement_value": getattr(record, 'measurement_value', None)
        })
        
        return entry