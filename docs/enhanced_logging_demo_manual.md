# enhanced_logging_demo.py - User Manual

## Overview
**File Path:** `examples/enhanced_logging_demo.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T09:12:36.863638  
**File Size:** 6,411 bytes  

## Description
Enhanced Logging Integration Demo for Framework0

This demo shows how to use the enhanced logging capabilities with
comprehensive I/O tracing, request correlation, and debug management.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 2.0.0-enhanced

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: demo_enhanced_logging**
2. **Function: demo_cross_component_integration**
3. **Data processing: process_data**
4. **Function: calculate_fibonacci**
5. **Data processing: process_scriptlet_data**
6. **Function: manage_tool_operation**

## Functions (6 total)

### `demo_enhanced_logging`

**Signature:** `demo_enhanced_logging()`  
**Line:** 25  
**Description:** Demonstrate comprehensive enhanced logging capabilities.

### `demo_cross_component_integration`

**Signature:** `demo_cross_component_integration()`  
**Line:** 93  
**Description:** Demonstrate cross-component logging integration.

### `process_data`

**Signature:** `process_data(input_text: str, multiplier: int) -> str`  
**Line:** 52  
**Description:** Example function with automatic I/O tracing.

### `calculate_fibonacci`

**Signature:** `calculate_fibonacci(n: int) -> int`  
**Line:** 65  
**Description:** Calculate fibonacci number with debug tracing.

### `process_scriptlet_data`

**Signature:** `process_scriptlet_data(data: str) -> str`  
**Line:** 118  
**Description:** Scriptlet processing with tracing.

### `manage_tool_operation`

**Signature:** `manage_tool_operation(operation: str) -> bool`  
**Line:** 123  
**Description:** Tool management with tracing.


## Usage Examples

```python
# Import the module
from examples.enhanced_logging_demo import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `os`
- `pathlib`
- `src.core.logger`
- `time`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
