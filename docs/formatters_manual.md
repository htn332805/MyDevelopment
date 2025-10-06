# formatters.py - User Manual

## Overview
**File Path:** `scriptlets/foundation/logging/formatters.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T13:32:27.050717  
**File Size:** 9,764 bytes  

## Description
Framework0 Foundation - Logging Formatters

Specialized formatters for different output formats and targets:
- ContextAwareFormatter for Framework0 integration
- JSON structured formatter for machine parsing
- Human-readable formatters for development and operations
- Error and exception formatting with stack traces

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __init__**
2. **Function: format**
3. **Function: _create_log_entry_from_record**
4. **Function: _format_as_json**
5. **Function: _format_as_simple_text**
6. **Function: _format_as_detailed_text**
7. **Function: _create_fallback_format**
8. **Function: __init__**
9. **Function: _create_log_entry_from_record**
10. **Function: __init__**
11. **Function: _create_log_entry_from_record**
12. **Class: ContextAwareFormatter (7 methods)**
13. **Class: AuditFormatter (2 methods)**
14. **Class: PerformanceFormatter (2 methods)**

## Functions (11 total)

### `__init__`

**Signature:** `__init__(self, format_type: LogFormat, include_context: bool) -> None`  
**Line:** 33  
**Description:** Initialize the context-aware formatter.

Args:
    format_type: The type of formatting to apply (JSON, text, etc.)
    include_context: Whether to include Framework0 context information

### `format`

**Signature:** `format(self, record: logging.LogRecord) -> str`  
**Line:** 45  
**Description:** Format log record with Framework0 context information.

Args:
    record: The log record to format
    
Returns:
    Formatted log message string

### `_create_log_entry_from_record`

**Signature:** `_create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry`  
**Line:** 71  
**Description:** Create structured LogEntry from logging.LogRecord.

Args:
    record: Standard logging record
    
Returns:
    Structured LogEntry with Framework0 context

### `_format_as_json`

**Signature:** `_format_as_json(self, entry: LogEntry) -> str`  
**Line:** 111  
**Description:** Format log entry as structured JSON.

Args:
    entry: Structured log entry
    
Returns:
    JSON formatted string

### `_format_as_simple_text`

**Signature:** `_format_as_simple_text(self, entry: LogEntry) -> str`  
**Line:** 129  
**Description:** Format log entry as simple readable text.

Args:
    entry: Structured log entry
    
Returns:
    Simple text formatted string

### `_format_as_detailed_text`

**Signature:** `_format_as_detailed_text(self, entry: LogEntry) -> str`  
**Line:** 142  
**Description:** Format log entry with detailed context information.

Args:
    entry: Structured log entry
    
Returns:
    Detailed text formatted string with context

### `_create_fallback_format`

**Signature:** `_create_fallback_format(self, record: logging.LogRecord, error: Exception) -> str`  
**Line:** 188  
**Description:** Create fallback format when normal formatting fails.

Args:
    record: Original log record
    error: Formatting error that occurred
    
Returns:
    Basic formatted string with error information

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 214  
**Description:** Initialize audit formatter with JSON format.

### `_create_log_entry_from_record`

**Signature:** `_create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry`  
**Line:** 218  
**Description:** Create audit log entry with additional compliance fields.

Args:
    record: Standard logging record
    
Returns:
    LogEntry enhanced for audit purposes

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 253  
**Description:** Initialize performance formatter with JSON format.

### `_create_log_entry_from_record`

**Signature:** `_create_log_entry_from_record(self, record: logging.LogRecord) -> LogEntry`  
**Line:** 257  
**Description:** Create performance log entry with metrics data.

Args:
    record: Standard logging record
    
Returns:
    LogEntry enhanced for performance analysis


## Classes (3 total)

### `ContextAwareFormatter`

**Line:** 22  
**Inherits from:** logging.Formatter  
**Description:** Custom formatter that includes Framework0 context in log entries.

Automatically extracts and includes contextual information:
- Recipe and step execution context
- Thread and process identification for parallel execution
- Execution tracking for distributed operations
- Custom extra data for specialized logging needs

**Methods (7 total):**
- `__init__`: Initialize the context-aware formatter.

Args:
    format_type: The type of formatting to apply (JSON, text, etc.)
    include_context: Whether to include Framework0 context information
- `format`: Format log record with Framework0 context information.

Args:
    record: The log record to format
    
Returns:
    Formatted log message string
- `_create_log_entry_from_record`: Create structured LogEntry from logging.LogRecord.

Args:
    record: Standard logging record
    
Returns:
    Structured LogEntry with Framework0 context
- `_format_as_json`: Format log entry as structured JSON.

Args:
    entry: Structured log entry
    
Returns:
    JSON formatted string
- `_format_as_simple_text`: Format log entry as simple readable text.

Args:
    entry: Structured log entry
    
Returns:
    Simple text formatted string
- `_format_as_detailed_text`: Format log entry with detailed context information.

Args:
    entry: Structured log entry
    
Returns:
    Detailed text formatted string with context
- `_create_fallback_format`: Create fallback format when normal formatting fails.

Args:
    record: Original log record
    error: Formatting error that occurred
    
Returns:
    Basic formatted string with error information

### `AuditFormatter`

**Line:** 205  
**Inherits from:** ContextAwareFormatter  
**Description:** Specialized formatter for audit logging with compliance focus.

Always uses structured JSON format for compliance and security analysis.
Includes additional audit-specific fields and ensures all required
information is captured for regulatory and security requirements.

**Methods (2 total):**
- `__init__`: Initialize audit formatter with JSON format.
- `_create_log_entry_from_record`: Create audit log entry with additional compliance fields.

Args:
    record: Standard logging record
    
Returns:
    LogEntry enhanced for audit purposes

### `PerformanceFormatter`

**Line:** 245  
**Inherits from:** ContextAwareFormatter  
**Description:** Specialized formatter for performance and metrics logging.

Optimized for performance data analysis and monitoring systems.
Includes timing information and resource utilization data.

**Methods (2 total):**
- `__init__`: Initialize performance formatter with JSON format.
- `_create_log_entry_from_record`: Create performance log entry with metrics data.

Args:
    record: Standard logging record
    
Returns:
    LogEntry enhanced for performance analysis


## Usage Examples

```python
# Import the module
from scriptlets.foundation.logging.formatters import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `core`
- `dataclasses`
- `json`
- `logging`
- `os`
- `threading`
- `traceback`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
