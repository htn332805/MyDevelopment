# registry.py - User Manual

## Overview
**File Path:** `src/analysis/registry.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T01:24:28.565871  
**File Size:** 18,677 bytes  

## Description
Analysis Registry System

This module provides dynamic analyzer discovery, registration, and 
instantiation capabilities for the consolidated analysis framework.
It enables flexible composition of analysis pipelines and supports
runtime analyzer loading and configuration.

Components:
    AnalysisRegistry: Central registry for analyzer management
    register_analyzer: Decorator for analyzer registration
    AnalyzerFactory: Factory for creating analyzer instances
    get_available_analyzers: Function to list registered analyzers

Features:
    - Dynamic analyzer discovery and loading
    - Thread-safe registry operations
    - Configuration validation and management
    - Dependency resolution for analyzer chains
    - Plugin-style analyzer extensions
    - Performance monitoring and caching

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Data analysis: register_analyzer**
2. **Data analysis: get_available_analyzers**
3. **Data analysis: discover_analyzers**
4. **Function: __init__**
5. **Data analysis: create_analyzer**
6. **Validation: _validate_config**
7. **Function: clear_cache**
8. **Data analysis: get_cached_analyzers**
9. **Function: register**
10. **Function: unregister**
11. **Data analysis: get_analyzer_info**
12. **Data analysis: get_available_analyzers**
13. **Data analysis: get_analyzer**
14. **Data analysis: create_analyzer_chain**
15. **Function: clear_registry**
16. **Function: decorator**
17. **Class: AnalyzerFactory (5 methods)**
18. **Class: AnalysisRegistry (7 methods)**

## Functions (16 total)

### `register_analyzer`

**Signature:** `register_analyzer(name: Optional[str], description: Optional[str], version: Optional[str], dependencies: Optional[List[str]], config_requirements: Optional[Dict[str, Any]]) -> Callable`  
**Line:** 337  
**Description:** Decorator for registering analyzer classes.

Args:
    name: Analyzer name (uses class name if None)
    description: Analyzer description
    version: Version string
    dependencies: List of dependencies
    config_requirements: Configuration requirements
    
Returns:
    Decorator function for analyzer class registration

### `get_available_analyzers`

**Signature:** `get_available_analyzers() -> Dict[str, str]`  
**Line:** 374  
**Description:** Get simple mapping of available analyzer names to descriptions.

Returns:
    Dictionary mapping analyzer names to descriptions

### `discover_analyzers`

**Signature:** `discover_analyzers(package_path: str) -> int`  
**Line:** 385  
**Description:** Automatically discover and register analyzers from specified package.

Args:
    package_path: Python package path to search for analyzers
    
Returns:
    Number of analyzers discovered and registered

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 54  
**Description:** Initialize analyzer factory with thread safety.

### `create_analyzer`

**Signature:** `create_analyzer(self, analyzer_name: str, config: Optional[AnalysisConfig], force_new: bool) -> BaseAnalyzerV2`  
**Line:** 62  
**Description:** Create analyzer instance with configuration and caching.

Args:
    analyzer_name: Name of analyzer to create
    config: Configuration for analyzer (uses defaults if None)
    force_new: Whether to force creation of new instance
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance
    
Raises:
    AnalysisError: If analyzer not found or creation fails

### `_validate_config`

**Signature:** `_validate_config(self, analyzer_name: str, config: AnalysisConfig, analyzer_info: Dict[str, Any]) -> None`  
**Line:** 122  
**Description:** Validate configuration against analyzer requirements.

### `clear_cache`

**Signature:** `clear_cache(self) -> None`  
**Line:** 154  
**Description:** Clear instance cache to free memory.

### `get_cached_analyzers`

**Signature:** `get_cached_analyzers(self) -> List[str]`  
**Line:** 161  
**Description:** Get list of cached analyzer names.

### `register`

**Signature:** `register(analyzer_name: str, analyzer_class: Type[BaseAnalyzerV2], description: Optional[str], version: Optional[str], dependencies: Optional[List[str]], config_requirements: Optional[Dict[str, Any]]) -> None`  
**Line:** 187  
**Description:** Register analyzer class in the global registry.

Args:
    analyzer_name: Unique name for the analyzer
    analyzer_class: Analyzer class (must inherit from BaseAnalyzerV2)
    description: Optional description of analyzer capabilities
    version: Version string for analyzer
    dependencies: List of required dependencies
    config_requirements: Configuration requirements specification

### `unregister`

**Signature:** `unregister(analyzer_name: str) -> bool`  
**Line:** 231  
**Description:** Unregister analyzer from registry.

Args:
    analyzer_name: Name of analyzer to remove
    
Returns:
    bool: True if analyzer was removed, False if not found

### `get_analyzer_info`

**Signature:** `get_analyzer_info(analyzer_name: str) -> Optional[Dict[str, Any]]`  
**Line:** 253  
**Description:** Get detailed information about registered analyzer.

Args:
    analyzer_name: Name of analyzer to query
    
Returns:
    Dictionary with analyzer information or None if not found

### `get_available_analyzers`

**Signature:** `get_available_analyzers() -> Dict[str, Dict[str, Any]]`  
**Line:** 269  
**Description:** Get dictionary of all registered analyzers with their metadata.

Returns:
    Dictionary mapping analyzer names to their information

### `get_analyzer`

**Signature:** `get_analyzer(analyzer_name: str, config: Optional[AnalysisConfig]) -> BaseAnalyzerV2`  
**Line:** 283  
**Description:** Get analyzer instance using factory pattern.

Args:
    analyzer_name: Name of analyzer to retrieve
    config: Configuration for analyzer
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance

### `create_analyzer_chain`

**Signature:** `create_analyzer_chain(analyzer_names: List[str], configs: Optional[List[AnalysisConfig]]) -> List[BaseAnalyzerV2]`  
**Line:** 297  
**Description:** Create chain of analyzers for pipeline processing.

Args:
    analyzer_names: List of analyzer names in execution order
    configs: Optional list of configurations (must match analyzer count)
    
Returns:
    List of configured analyzer instances

### `clear_registry`

**Signature:** `clear_registry() -> None`  
**Line:** 326  
**Description:** Clear all registered analyzers (primarily for testing).

### `decorator`

**Signature:** `decorator(analyzer_class: Type[BaseAnalyzerV2]) -> Type[BaseAnalyzerV2]`  
**Line:** 355  
**Description:** Function: decorator


## Classes (2 total)

### `AnalyzerFactory`

**Line:** 46  
**Description:** Factory class for creating analyzer instances with configuration validation.

Provides standardized analyzer instantiation with configuration management,
dependency resolution, and performance monitoring capabilities.

**Methods (5 total):**
- `__init__`: Initialize analyzer factory with thread safety.
- `create_analyzer`: Create analyzer instance with configuration and caching.

Args:
    analyzer_name: Name of analyzer to create
    config: Configuration for analyzer (uses defaults if None)
    force_new: Whether to force creation of new instance
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance
    
Raises:
    AnalysisError: If analyzer not found or creation fails
- `_validate_config`: Validate configuration against analyzer requirements.
- `clear_cache`: Clear instance cache to free memory.
- `get_cached_analyzers`: Get list of cached analyzer names.

### `AnalysisRegistry`

**Line:** 171  
**Description:** Central registry for analyzer discovery, registration, and management.

Provides thread-safe operations for registering analyzers, retrieving
analyzer information, and managing analyzer lifecycle.

Features:
    - Thread-safe registration and lookup
    - Analyzer metadata management
    - Dependency tracking and resolution
    - Plugin-style extensions
    - Performance monitoring

**Methods (7 total):**
- `register`: Register analyzer class in the global registry.

Args:
    analyzer_name: Unique name for the analyzer
    analyzer_class: Analyzer class (must inherit from BaseAnalyzerV2)
    description: Optional description of analyzer capabilities
    version: Version string for analyzer
    dependencies: List of required dependencies
    config_requirements: Configuration requirements specification
- `unregister`: Unregister analyzer from registry.

Args:
    analyzer_name: Name of analyzer to remove
    
Returns:
    bool: True if analyzer was removed, False if not found
- `get_analyzer_info`: Get detailed information about registered analyzer.

Args:
    analyzer_name: Name of analyzer to query
    
Returns:
    Dictionary with analyzer information or None if not found
- `get_available_analyzers`: Get dictionary of all registered analyzers with their metadata.

Returns:
    Dictionary mapping analyzer names to their information
- `get_analyzer`: Get analyzer instance using factory pattern.

Args:
    analyzer_name: Name of analyzer to retrieve
    config: Configuration for analyzer
    
Returns:
    BaseAnalyzerV2: Configured analyzer instance
- `create_analyzer_chain`: Create chain of analyzers for pipeline processing.

Args:
    analyzer_names: List of analyzer names in execution order
    configs: Optional list of configurations (must match analyzer count)
    
Returns:
    List of configured analyzer instances
- `clear_registry`: Clear all registered analyzers (primarily for testing).


## Usage Examples

```python
# Import the module
from src.analysis.registry import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `datetime`
- `framework`
- `importlib`
- `os`
- `pathlib`
- `src.analysis.framework`
- `src.core.logger`
- `threading`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
