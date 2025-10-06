# health_integration_test - Recipe Manual

## Overview
**File Path:** `recipes/health_integration_test.yaml`  
**File Type:** Recipe Configuration  
**Last Modified:** 2025-10-05T13:32:27.150716  
**File Size:** 1,580 bytes  

## Description
Recipe configuration: health_integration_test

## Purpose and Application
This recipe file is part of the Framework0 Recipe Execution Engine and defines:

### Recipe Components
1. **Step: setup_health_monitoring (module: scriptlets.foundation.health_monitoring)**
2. **Step: run_health_checks (module: scriptlets.foundation.health_monitoring)**
3. **Step: generate_health_report (module: scriptlets.foundation.health_monitoring)**
4. **Step: validate_health_system (module: engine.steps.python.test_health_monitoring)**

## Usage

### Recipe Execution
```bash
python orchestrator/runner.py --recipe recipes/health_integration_test.yaml
```


## Required Modules

This recipe requires the following modules:

- `engine.steps.python.test_health_monitoring`
- `scriptlets.foundation.health_monitoring`


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
