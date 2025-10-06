# test_missing - Recipe Manual

## Overview
**File Path:** `orchestrator/recipes/test_missing.yaml`  
**File Type:** Recipe Configuration  
**Last Modified:** 2025-10-05T11:20:35.225528  
**File Size:** 265 bytes  

## Description
Test recipe with missing dependencies to verify CLI notification

## Purpose and Application
This recipe file is part of the Framework0 Recipe Execution Engine and defines:

### Recipe Components
1. **Step: missing_step (module: engine.steps.python.missing_module)**
2. **Recipe name: test_missing_dependencies**

## Usage

### Recipe Execution
```bash
python orchestrator/runner.py --recipe orchestrator/recipes/test_missing.yaml
```


## Required Modules

This recipe requires the following modules:

- `engine.steps.python.missing_module`


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
