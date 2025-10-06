# interactive_demo.py - User Manual

## Overview
**File Path:** `capstone/integration/interactive_demo.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T20:41:32.352137  
**File Size:** 38,943 bytes  

## Description
Interactive System Demo - Phase 8
Framework0 Capstone Project - Complete System Integration Demonstration

This module provides a comprehensive interactive demonstration showcasing
the complete Framework0 capstone integration across all 8 phases, with
user interaction, real-time visualization, and complete system walkthrough.

Author: Framework0 Team
Date: October 5, 2025

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: __post_init__**
2. **Function: __init__**
3. **Function: display_welcome_screen**
4. **Function: display_demo_menu**
5. **Function: wait_for_user_input**
6. **Function: display_performance_summary**
7. **Function: display_conclusion**
8. **Class: DemoMode (0 methods)**
9. **Class: DemoSection (0 methods)**
10. **Class: DemoProgress (1 methods)**
11. **Class: InteractiveSystemDemo (6 methods)**

## Functions (7 total)

### `__post_init__`

**Signature:** `__post_init__(self)`  
**Line:** 65  
**Description:** Function: __post_init__

### `__init__`

**Signature:** `__init__(self)`  
**Line:** 79  
**Description:** Initialize interactive system demonstration.

### `display_welcome_screen`

**Signature:** `display_welcome_screen(self) -> None`  
**Line:** 101  
**Description:** Display welcome screen and demo overview.

### `display_demo_menu`

**Signature:** `display_demo_menu(self) -> DemoMode`  
**Line:** 137  
**Description:** Display demonstration mode selection menu.

### `wait_for_user_input`

**Signature:** `wait_for_user_input(self, prompt: str) -> str`  
**Line:** 173  
**Description:** Wait for user input with optional prompt.

### `display_performance_summary`

**Signature:** `display_performance_summary(self) -> Dict[str, Any]`  
**Line:** 658  
**Description:** Display comprehensive performance summary.

### `display_conclusion`

**Signature:** `display_conclusion(self) -> None`  
**Line:** 703  
**Description:** Display demonstration conclusion.


## Classes (4 total)

### `DemoMode`

**Line:** 32  
**Inherits from:** Enum  
**Description:** Enumeration of demonstration modes.

### `DemoSection`

**Line:** 41  
**Inherits from:** Enum  
**Description:** Enumeration of demonstration sections.

### `DemoProgress`

**Line:** 57  
**Description:** Data class tracking demonstration progress.

**Methods (1 total):**
- `__post_init__`: Function: __post_init__

### `InteractiveSystemDemo`

**Line:** 70  
**Description:** Interactive system demonstration for complete Framework0 capstone showcase.

This class provides a comprehensive, interactive demonstration of all
Framework0 capstone phases with user interaction, real-time visualization,
and complete system integration showcase.

**Methods (6 total):**
- `__init__`: Initialize interactive system demonstration.
- `display_welcome_screen`: Display welcome screen and demo overview.
- `display_demo_menu`: Display demonstration mode selection menu.
- `wait_for_user_input`: Wait for user input with optional prompt.
- `display_performance_summary`: Display comprehensive performance summary.
- `display_conclusion`: Display demonstration conclusion.


## Usage Examples

```python
# Import the module
from capstone.integration.interactive_demo import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `asyncio`
- `dataclasses`
- `datetime`
- `enum`
- `json`
- `pathlib`
- `src.core.logger`
- `sys`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
