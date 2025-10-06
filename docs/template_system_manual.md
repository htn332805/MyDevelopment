# template_system.py - User Manual

## Overview
**File Path:** `scriptlets/extensions/template_system.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-05T18:11:37.158333  
**File Size:** 37,279 bytes  

## Description
Framework0 Template System - Exercise 10 Phase 4

This module provides comprehensive template management for Framework0,
enabling dynamic content generation with Jinja2 engine, template inheritance,
context management, custom filters/functions, and integration with configuration
and event systems.

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: create_template_manager**
2. **Function: render_string_template**
3. **Function: get_template_manager**
4. **Function: set_global_template_manager**
5. **Function: __call__**
6. **Function: __call__**
7. **Function: __post_init__**
8. **Function: update**
9. **Function: set_variable**
10. **Function: get_variable**
11. **Function: add_filter**
12. **Function: add_function**
13. **Function: load_template**
14. **Function: list_templates**
15. **Function: template_exists**
16. **Function: __init__**
17. **Function: load_template**
18. **Function: list_templates**
19. **Function: template_exists**
20. **Function: save_template**
21. **Function: __init__**
22. **Function: load_template**
23. **Function: list_templates**
24. **Function: template_exists**
25. **Function: add_template**
26. **Function: remove_template**
27. **Function: __init__**
28. **Function: _setup_jinja_environment**
29. **Function: _register_builtin_filters**
30. **Function: _register_builtin_functions**
31. **Function: add_filter**
32. **Function: add_function**
33. **Function: compile_template**
34. **Function: render_template**
35. **Validation: validate_template**
36. **Function: list_templates**
37. **Function: get_template_metadata**
38. **Function: clear_cache**
39. **Function: __init__**
40. **Function: _setup_default_engines**
41. **Function: _setup_event_handlers**
42. **Function: _load_template_configuration**
43. **Function: add_engine**
44. **Function: get_engine**
45. **Function: render_template**
46. **Function: create_template**
47. **Function: list_templates**
48. **Validation: validate_template**
49. **Function: add_global_variable**
50. **Function: add_global_filter**
51. **Function: add_global_function**
52. **Function: clear_all_caches**
53. **Function: template_context**
54. **Function: timestamp_filter**
55. **Function: json_filter**
56. **Function: yaml_filter**
57. **Function: upper_first_filter**
58. **Function: snake_case_filter**
59. **Function: camel_case_filter**
60. **Function: now_function**
61. **Function: env_function**
62. **Function: range_function**
63. **Function: len_function**
64. **Function: format_function**
65. **Function: config_change_handler**
66. **Function: __init__**
67. **Function: get_source**
68. **Class: TemplateFilter (1 methods)**
69. **Class: TemplateFunction (1 methods)**
70. **Class: TemplateMetadata (1 methods)**
71. **Class: TemplateContext (5 methods)**
72. **Class: TemplateError (0 methods)**
73. **Class: TemplateNotFoundError (0 methods)**
74. **Class: TemplateRenderError (0 methods)**
75. **Class: TemplateValidationError (0 methods)**
76. **Class: TemplateLoader (3 methods)**
77. **Class: FileSystemTemplateLoader (5 methods)**
78. **Class: InMemoryTemplateLoader (6 methods)**
79. **Class: TemplateEngine (12 methods)**
80. **Class: TemplateManager (15 methods)**
81. **Class: Environment (0 methods)**
82. **Class: FileSystemLoader (0 methods)**
83. **Class: DictLoader (0 methods)**
84. **Class: BaseLoader (0 methods)**
85. **Class: Template (0 methods)**
86. **Class: TemplateNotFound (0 methods)**
87. **Class: TemplateSyntaxError (0 methods)**
88. **Class: UndefinedError (0 methods)**
89. **Class: CustomJinjaLoader (2 methods)**

## Functions (67 total)

### `create_template_manager`

**Signature:** `create_template_manager(template_dirs: Optional[List[Path]], auto_reload: bool, enable_events: bool) -> TemplateManager`  
**Line:** 981  
**Description:** Factory function to create configured template manager.

Args:
    template_dirs: Template directories to search
    auto_reload: Auto-reload changed templates
    enable_events: Enable event system integration
    
Returns:
    TemplateManager: Configured template manager

### `render_string_template`

**Signature:** `render_string_template(template_string: str) -> str`  
**Line:** 1004  
**Description:** Render template string with variables.

Args:
    template_string: Template content as string
    **variables: Template variables
    
Returns:
    str: Rendered template

### `get_template_manager`

**Signature:** `get_template_manager() -> TemplateManager`  
**Line:** 1026  
**Description:** Get or create global template manager instance.

Returns:
    TemplateManager: Global template manager

### `set_global_template_manager`

**Signature:** `set_global_template_manager(template_manager: TemplateManager) -> None`  
**Line:** 1042  
**Description:** Set global template manager instance.

Args:
    template_manager: Template manager to use as global instance

### `__call__`

**Signature:** `__call__(self, value: Any) -> Any`  
**Line:** 85  
**Description:** Apply filter to value.

### `__call__`

**Signature:** `__call__(self) -> Any`  
**Line:** 94  
**Description:** Execute template function.

### `__post_init__`

**Signature:** `__post_init__(self) -> None`  
**Line:** 114  
**Description:** Post-initialization setup.

### `update`

**Signature:** `update(self, context: 'TemplateContext') -> 'TemplateContext'`  
**Line:** 129  
**Description:** Update context with another context.

### `set_variable`

**Signature:** `set_variable(self, name: str, value: Any) -> None`  
**Line:** 148  
**Description:** Set template variable.

### `get_variable`

**Signature:** `get_variable(self, name: str, default: Any) -> Any`  
**Line:** 152  
**Description:** Get template variable.

### `add_filter`

**Signature:** `add_filter(self, name: str, filter_func: TemplateFilter) -> None`  
**Line:** 156  
**Description:** Add custom filter function.

### `add_function`

**Signature:** `add_function(self, name: str, function: TemplateFunction) -> None`  
**Line:** 160  
**Description:** Add custom global function.

### `load_template`

**Signature:** `load_template(self, name: str) -> str`  
**Line:** 189  
**Description:** Load template source by name.

### `list_templates`

**Signature:** `list_templates(self) -> List[str]`  
**Line:** 194  
**Description:** List all available templates.

### `template_exists`

**Signature:** `template_exists(self, name: str) -> bool`  
**Line:** 199  
**Description:** Check if template exists.

### `__init__`

**Signature:** `__init__(self, template_dirs: List[Path], encoding: str) -> None`  
**Line:** 207  
**Description:** Initialize filesystem template loader.

Args:
    template_dirs: List of template directories to search
    encoding: File encoding for template files

### `load_template`

**Signature:** `load_template(self, name: str) -> str`  
**Line:** 223  
**Description:** Load template from filesystem.

### `list_templates`

**Signature:** `list_templates(self) -> List[str]`  
**Line:** 237  
**Description:** List all template files.

### `template_exists`

**Signature:** `template_exists(self, name: str) -> bool`  
**Line:** 251  
**Description:** Check if template exists in any directory.

### `save_template`

**Signature:** `save_template(self, name: str, content: str) -> Path`  
**Line:** 259  
**Description:** Save template to first template directory.

### `__init__`

**Signature:** `__init__(self) -> None`  
**Line:** 276  
**Description:** Initialize in-memory template loader.

### `load_template`

**Signature:** `load_template(self, name: str) -> str`  
**Line:** 281  
**Description:** Load template from memory.

### `list_templates`

**Signature:** `list_templates(self) -> List[str]`  
**Line:** 288  
**Description:** List all templates in memory.

### `template_exists`

**Signature:** `template_exists(self, name: str) -> bool`  
**Line:** 292  
**Description:** Check if template exists in memory.

### `add_template`

**Signature:** `add_template(self, name: str, content: str) -> None`  
**Line:** 296  
**Description:** Add template to memory.

### `remove_template`

**Signature:** `remove_template(self, name: str) -> bool`  
**Line:** 301  
**Description:** Remove template from memory.

### `__init__`

**Signature:** `__init__(self, loader: TemplateLoader, auto_reload: bool, enable_async: bool, strict_undefined: bool) -> None`  
**Line:** 318  
**Description:** Initialize template engine.

Args:
    loader: Template loader for template source
    auto_reload: Whether to auto-reload changed templates
    enable_async: Enable async template rendering
    strict_undefined: Raise errors on undefined variables

### `_setup_jinja_environment`

**Signature:** `_setup_jinja_environment(self) -> None`  
**Line:** 358  
**Description:** Setup Jinja2 environment with custom loader.

### `_register_builtin_filters`

**Signature:** `_register_builtin_filters(self) -> None`  
**Line:** 384  
**Description:** Register built-in template filters.

### `_register_builtin_functions`

**Signature:** `_register_builtin_functions(self) -> None`  
**Line:** 439  
**Description:** Register built-in template global functions.

### `add_filter`

**Signature:** `add_filter(self, name: str, filter_func: TemplateFilter) -> None`  
**Line:** 480  
**Description:** Add custom template filter.

### `add_function`

**Signature:** `add_function(self, name: str, function: TemplateFunction) -> None`  
**Line:** 485  
**Description:** Add custom global function.

### `compile_template`

**Signature:** `compile_template(self, name: str, force_reload: bool) -> Template`  
**Line:** 490  
**Description:** Compile template and cache result.

Args:
    name: Template name
    force_reload: Force reload from source
    
Returns:
    Template: Compiled Jinja2 template

### `render_template`

**Signature:** `render_template(self, name: str, context: Optional[TemplateContext]) -> str`  
**Line:** 532  
**Description:** Render template with context.

Args:
    name: Template name
    context: Template context with variables
    **kwargs: Additional template variables
    
Returns:
    str: Rendered template content

### `validate_template`

**Signature:** `validate_template(self, name: str) -> bool`  
**Line:** 580  
**Description:** Validate template syntax.

Args:
    name: Template name to validate
    
Returns:
    bool: True if template is valid

### `list_templates`

**Signature:** `list_templates(self) -> List[str]`  
**Line:** 596  
**Description:** List all available templates.

### `get_template_metadata`

**Signature:** `get_template_metadata(self, name: str) -> Optional[TemplateMetadata]`  
**Line:** 600  
**Description:** Get template metadata.

### `clear_cache`

**Signature:** `clear_cache(self) -> None`  
**Line:** 604  
**Description:** Clear template cache.

### `__init__`

**Signature:** `__init__(self, template_dirs: Optional[List[Path]], auto_reload: bool, enable_events: bool) -> None`  
**Line:** 619  
**Description:** Initialize template manager.

Args:
    template_dirs: Template directories to search
    auto_reload: Auto-reload changed templates
    enable_events: Enable event system integration

### `_setup_default_engines`

**Signature:** `_setup_default_engines(self) -> None`  
**Line:** 676  
**Description:** Setup default template engines.

### `_setup_event_handlers`

**Signature:** `_setup_event_handlers(self) -> None`  
**Line:** 693  
**Description:** Setup event system handlers for template events.

### `_load_template_configuration`

**Signature:** `_load_template_configuration(self) -> None`  
**Line:** 718  
**Description:** Load template system configuration.

### `add_engine`

**Signature:** `add_engine(self, name: str, engine: TemplateEngine, loader: TemplateLoader) -> None`  
**Line:** 739  
**Description:** Add template engine.

### `get_engine`

**Signature:** `get_engine(self, name: str) -> TemplateEngine`  
**Line:** 750  
**Description:** Get template engine by name.

### `render_template`

**Signature:** `render_template(self, template_name: str, context: Optional[TemplateContext], engine_name: str) -> str`  
**Line:** 756  
**Description:** Render template with context.

Args:
    template_name: Name of template to render
    context: Template context
    engine_name: Template engine to use
    **kwargs: Additional template variables
    
Returns:
    str: Rendered template content

### `create_template`

**Signature:** `create_template(self, name: str, content: str, engine_name: str, metadata: Optional[TemplateMetadata]) -> Path`  
**Line:** 840  
**Description:** Create new template.

Args:
    name: Template name
    content: Template content
    engine_name: Engine to save template to
    metadata: Template metadata
    
Returns:
    Path: Path where template was saved (if filesystem)

### `list_templates`

**Signature:** `list_templates(self, engine_name: str) -> List[str]`  
**Line:** 917  
**Description:** List templates in engine.

### `validate_template`

**Signature:** `validate_template(self, name: str, engine_name: str) -> bool`  
**Line:** 922  
**Description:** Validate template syntax.

### `add_global_variable`

**Signature:** `add_global_variable(self, name: str, value: Any) -> None`  
**Line:** 927  
**Description:** Add global template variable.

### `add_global_filter`

**Signature:** `add_global_filter(self, name: str, filter_func: TemplateFilter) -> None`  
**Line:** 932  
**Description:** Add global template filter to all engines.

### `add_global_function`

**Signature:** `add_global_function(self, name: str, function: TemplateFunction) -> None`  
**Line:** 942  
**Description:** Add global template function to all engines.

### `clear_all_caches`

**Signature:** `clear_all_caches(self) -> None`  
**Line:** 952  
**Description:** Clear all template caches.

### `template_context`

**Signature:** `template_context(self)`  
**Line:** 959  
**Description:** Context manager for temporary template variables.

### `timestamp_filter`

**Signature:** `timestamp_filter(value: datetime) -> str`  
**Line:** 387  
**Description:** Format datetime as timestamp.

### `json_filter`

**Signature:** `json_filter(value: Any) -> str`  
**Line:** 393  
**Description:** Convert value to JSON string.

### `yaml_filter`

**Signature:** `yaml_filter(value: Any) -> str`  
**Line:** 397  
**Description:** Convert value to YAML string.

### `upper_first_filter`

**Signature:** `upper_first_filter(value: str) -> str`  
**Line:** 401  
**Description:** Capitalize first letter only.

### `snake_case_filter`

**Signature:** `snake_case_filter(value: str) -> str`  
**Line:** 407  
**Description:** Convert string to snake_case.

### `camel_case_filter`

**Signature:** `camel_case_filter(value: str) -> str`  
**Line:** 417  
**Description:** Convert string to camelCase.

### `now_function`

**Signature:** `now_function() -> datetime`  
**Line:** 442  
**Description:** Get current datetime.

### `env_function`

**Signature:** `env_function(name: str, default: str) -> str`  
**Line:** 446  
**Description:** Get environment variable.

### `range_function`

**Signature:** `range_function() -> range`  
**Line:** 450  
**Description:** Create range object (similar to Python range).

### `len_function`

**Signature:** `len_function(obj: Any) -> int`  
**Line:** 454  
**Description:** Get length of object.

### `format_function`

**Signature:** `format_function(template_str: str) -> str`  
**Line:** 461  
**Description:** Format string with arguments.

### `config_change_handler`

**Signature:** `config_change_handler(event: Event) -> str`  
**Line:** 699  
**Description:** Handle configuration change events.

### `__init__`

**Signature:** `__init__(self, template_loader: TemplateLoader)`  
**Line:** 364  
**Description:** Function: __init__

### `get_source`

**Signature:** `get_source(self, environment, template)`  
**Line:** 367  
**Description:** Function: get_source


## Classes (22 total)

### `TemplateFilter`

**Line:** 82  
**Inherits from:** Protocol  
**Description:** Protocol for template filter functions.

**Methods (1 total):**
- `__call__`: Apply filter to value.

### `TemplateFunction`

**Line:** 91  
**Inherits from:** Protocol  
**Description:** Protocol for template global functions.

**Methods (1 total):**
- `__call__`: Execute template function.

### `TemplateMetadata`

**Line:** 100  
**Description:** Template metadata for tracking and management.

**Methods (1 total):**
- `__post_init__`: Post-initialization setup.

### `TemplateContext`

**Line:** 121  
**Description:** Template rendering context with variable management.

**Methods (5 total):**
- `update`: Update context with another context.
- `set_variable`: Set template variable.
- `get_variable`: Get template variable.
- `add_filter`: Add custom filter function.
- `add_function`: Add custom global function.

### `TemplateError`

**Line:** 165  
**Inherits from:** Exception  
**Description:** Base exception for template system errors.

### `TemplateNotFoundError`

**Line:** 170  
**Inherits from:** TemplateError  
**Description:** Template not found exception.

### `TemplateRenderError`

**Line:** 175  
**Inherits from:** TemplateError  
**Description:** Template rendering exception.

### `TemplateValidationError`

**Line:** 180  
**Inherits from:** TemplateError  
**Description:** Template validation exception.

### `TemplateLoader`

**Line:** 185  
**Inherits from:** ABC  
**Description:** Abstract base class for template loaders.

**Methods (3 total):**
- `load_template`: Load template source by name.
- `list_templates`: List all available templates.
- `template_exists`: Check if template exists.

### `FileSystemTemplateLoader`

**Line:** 204  
**Inherits from:** TemplateLoader  
**Description:** File system-based template loader.

**Methods (5 total):**
- `__init__`: Initialize filesystem template loader.

Args:
    template_dirs: List of template directories to search
    encoding: File encoding for template files
- `load_template`: Load template from filesystem.
- `list_templates`: List all template files.
- `template_exists`: Check if template exists in any directory.
- `save_template`: Save template to first template directory.

### `InMemoryTemplateLoader`

**Line:** 273  
**Inherits from:** TemplateLoader  
**Description:** In-memory template loader for dynamic templates.

**Methods (6 total):**
- `__init__`: Initialize in-memory template loader.
- `load_template`: Load template from memory.
- `list_templates`: List all templates in memory.
- `template_exists`: Check if template exists in memory.
- `add_template`: Add template to memory.
- `remove_template`: Remove template from memory.

### `TemplateEngine`

**Line:** 310  
**Description:** Advanced template engine with Jinja2 integration.

Provides template compilation, rendering, inheritance, and custom
filter/function support with comprehensive error handling.

**Methods (12 total):**
- `__init__`: Initialize template engine.

Args:
    loader: Template loader for template source
    auto_reload: Whether to auto-reload changed templates
    enable_async: Enable async template rendering
    strict_undefined: Raise errors on undefined variables
- `_setup_jinja_environment`: Setup Jinja2 environment with custom loader.
- `_register_builtin_filters`: Register built-in template filters.
- `_register_builtin_functions`: Register built-in template global functions.
- `add_filter`: Add custom template filter.
- `add_function`: Add custom global function.
- `compile_template`: Compile template and cache result.

Args:
    name: Template name
    force_reload: Force reload from source
    
Returns:
    Template: Compiled Jinja2 template
- `render_template`: Render template with context.

Args:
    name: Template name
    context: Template context with variables
    **kwargs: Additional template variables
    
Returns:
    str: Rendered template content
- `validate_template`: Validate template syntax.

Args:
    name: Template name to validate
    
Returns:
    bool: True if template is valid
- `list_templates`: List all available templates.
- `get_template_metadata`: Get template metadata.
- `clear_cache`: Clear template cache.

### `TemplateManager`

**Line:** 611  
**Description:** Comprehensive template management system.

Manages template engines, contexts, events, and integration
with Framework0 configuration and event systems.

**Methods (15 total):**
- `__init__`: Initialize template manager.

Args:
    template_dirs: Template directories to search
    auto_reload: Auto-reload changed templates
    enable_events: Enable event system integration
- `_setup_default_engines`: Setup default template engines.
- `_setup_event_handlers`: Setup event system handlers for template events.
- `_load_template_configuration`: Load template system configuration.
- `add_engine`: Add template engine.
- `get_engine`: Get template engine by name.
- `render_template`: Render template with context.

Args:
    template_name: Name of template to render
    context: Template context
    engine_name: Template engine to use
    **kwargs: Additional template variables
    
Returns:
    str: Rendered template content
- `create_template`: Create new template.

Args:
    name: Template name
    content: Template content
    engine_name: Engine to save template to
    metadata: Template metadata
    
Returns:
    Path: Path where template was saved (if filesystem)
- `list_templates`: List templates in engine.
- `validate_template`: Validate template syntax.
- `add_global_variable`: Add global template variable.
- `add_global_filter`: Add global template filter to all engines.
- `add_global_function`: Add global template function to all engines.
- `clear_all_caches`: Clear all template caches.
- `template_context`: Context manager for temporary template variables.

### `Environment`

**Line:** 39  
**Description:** Class: Environment

### `FileSystemLoader`

**Line:** 41  
**Description:** Class: FileSystemLoader

### `DictLoader`

**Line:** 43  
**Description:** Class: DictLoader

### `BaseLoader`

**Line:** 45  
**Description:** Class: BaseLoader

### `Template`

**Line:** 47  
**Description:** Class: Template

### `TemplateNotFound`

**Line:** 49  
**Inherits from:** Exception  
**Description:** Class: TemplateNotFound

### `TemplateSyntaxError`

**Line:** 51  
**Inherits from:** Exception  
**Description:** Class: TemplateSyntaxError

### `UndefinedError`

**Line:** 53  
**Inherits from:** Exception  
**Description:** Class: UndefinedError

### `CustomJinjaLoader`

**Line:** 361  
**Inherits from:** BaseLoader  
**Description:** Custom Jinja2 loader that uses our template loader.

**Methods (2 total):**
- `__init__`: Function: __init__
- `get_source`: Function: get_source


## Usage Examples

```python
# Import the module
from scriptlets.extensions.template_system import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `abc`
- `contextlib`
- `dataclasses`
- `datetime`
- `jinja2`
- `json`
- `os`
- `pathlib`
- `re`
- `scriptlets.extensions.configuration_system`
- `scriptlets.extensions.event_system`
- `shutil`
- `src.core.logger`
- `tempfile`
- `threading`
- `typing`
- `yaml`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
