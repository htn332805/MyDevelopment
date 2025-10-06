# integration_logging_test - Recipe Manual

## Overview
**File Path:** `recipes/integration_logging_test.yaml`  
**File Type:** Recipe Configuration  
**Last Modified:** 2025-10-05T13:32:27.146716  
**File Size:** 864 bytes  

## Description
Recipe configuration: integration_logging_test

## Purpose and Application
This recipe file is part of the Framework0 Recipe Execution Engine and defines:

### Recipe Components
1. **Step: setup_logging_framework (module: scriptlets.foundation.logging_framework)**
2. **Step: test_logging_usage (module: engine.steps.python.test_logging_framework)**

## Usage

### Recipe Execution
```bash
python orchestrator/runner.py --recipe recipes/integration_logging_test.yaml
```


## Required Modules

This recipe requires the following modules:

- `engine.steps.python.test_logging_framework`
- `scriptlets.foundation.logging_framework`


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
