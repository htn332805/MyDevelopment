# test_comprehensive_missing - Recipe Manual

## Overview
**File Path:** `orchestrator/recipes/test_comprehensive_missing.yaml`  
**File Type:** Recipe Configuration  
**Last Modified:** 2025-10-05T11:20:35.225528  
**File Size:** 554 bytes  

## Description
Recipe configuration: test_comprehensive_missing

## Purpose and Application
This recipe file is part of the Framework0 Recipe Execution Engine and defines:

### Recipe Components
1. **Step: load_missing_data (module: engine.steps.python.missing_module)**
2. **Step: use_missing_scriptlet (module: scriptlets.missing_scriptlet)**

## Usage

### Recipe Execution
```bash
python orchestrator/runner.py --recipe orchestrator/recipes/test_comprehensive_missing.yaml
```


## Required Modules

This recipe requires the following modules:

- `engine.steps.python.missing_module`
- `scriptlets.missing_scriptlet`


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
