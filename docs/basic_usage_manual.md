# basic_usage.py - User Manual

## Overview
**File Path:** `src/basic_usage.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T16:23:42.071527  
**File Size:** 4,169 bytes  

## Description
Basic Usage Example - IAF0 Framework Integration
==============================    # 6. Show Context history
    print("\n📊 Context Change History:")
    history = context.get_history()
    for i, change in enumerate(history[-5:], 1):  # Show last 5 changes
        print(f"  {i}. Change: {change}")=============
Demonstrates how to use Context, Scriptlet, and Analysis frameworks together.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: main**
2. **Function: __init__**
3. **Function: run**
4. **Data analysis: _analyze_impl**
5. **Class: DataProcessor (2 methods)**
6. **Class: CustomAnalyzer (1 methods)**

## Functions (4 total)

### `main`

**Signature:** `main()`  
**Line:** 79  
**Description:** Demonstrate integrated usage of IAF0 frameworks.

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 25  
**Description:** Initialize the processor.

### `run`

**Signature:** `run(self, input_data)`  
**Line:** 30  
**Description:** Process input data and store results in context.

### `_analyze_impl`

**Signature:** `_analyze_impl(self, data, config)`  
**Line:** 51  
**Description:** Internal analysis implementation required by base class.


## Classes (2 total)

### `DataProcessor`

**Line:** 22  
**Inherits from:** BaseScriptlet  
**Description:** Example scriptlet for data processing.

**Methods (2 total):**
- `__init__`: Initialize the processor.
- `run`: Process input data and store results in context.

### `CustomAnalyzer`

**Line:** 48  
**Inherits from:** BaseAnalyzerV2  
**Description:** Example analyzer for statistical analysis.

**Methods (1 total):**
- `_analyze_impl`: Internal analysis implementation required by base class.


## Usage Examples

```python
# Import the module
from src.basic_usage import *

# Execute main function
main()
```


## Dependencies

This module requires the following dependencies:

- `orchestrator.context.context`
- `os`
- `scriptlets.framework`
- `src.analysis.framework`
- `sys`


## Entry Points

The following functions can be used as entry points:

- `main()` - Main execution function
- `run()` - Main execution function


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
