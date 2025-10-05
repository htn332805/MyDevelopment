# orchestrator/enhanced_recipe_parser.py
"""
Enhanced Recipe Parser with Context Integration and Advanced Features.

This module provides an advanced recipe parsing system that integrates with the
Framework0 Context system, supports multiple formats (YAML/JSON), includes
comprehensive schema validation, and provides enhanced error handling.

Framework0 Integration Guidelines:
- Single responsibility: focused recipe parsing and validation
- Backward compatibility: maintains interface compatibility with existing recipe_parser
- Full Context integration: leverages Context system for data sharing and logging
- Comprehensive typing and documentation: every method fully typed and documented
- Extensible architecture: supports custom validators and format handlers
"""

import json
import os
import re
import importlib
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Callable, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

import yaml

from orchestrator.context.context import Context
from src.core.logger import get_logger

# Initialize logger with debug support
logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")


class RecipeFormat(Enum):
    """Supported recipe file formats."""
    YAML = "yaml"
    JSON = "json"
    YML = "yml"


class ValidationSeverity(Enum):
    """Validation message severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationMessage:
    """Container for validation messages with location and severity."""
    
    severity: ValidationSeverity  # Message severity level
    message: str  # Human-readable validation message
    location: str  # Location in recipe where issue occurred
    code: Optional[str] = None  # Optional error/warning code
    
    def __str__(self) -> str:
        """Return formatted validation message."""
        prefix = self.severity.value.upper()
        code_str = f" [{self.code}]" if self.code else ""
        return f"{prefix}{code_str} at {self.location}: {self.message}"


@dataclass
class RecipeMetadata:
    """Container for recipe metadata information."""
    
    name: str  # Recipe name
    version: str = "1.0"  # Recipe version
    description: str = ""  # Recipe description
    author: str = ""  # Recipe author
    created: Optional[datetime] = None  # Creation timestamp
    modified: Optional[datetime] = None  # Last modification timestamp
    tags: List[str] = field(default_factory=list)  # Recipe tags
    requirements: List[str] = field(default_factory=list)  # Required modules/packages


@dataclass
class StepInfo:
    """Container for parsed step information with validation."""
    
    name: str  # Step name/identifier
    idx: int  # Step execution order index
    step_type: str  # Step type (python, shell, etc.)
    module: str  # Python module to import
    function: str  # Function/class to execute
    args: Dict[str, Any] = field(default_factory=dict)  # Step arguments
    depends_on: List[str] = field(default_factory=list)  # Step dependencies
    success_criteria: Dict[str, Any] = field(default_factory=dict)  # Success validation
    timeout: Optional[float] = None  # Execution timeout in seconds
    retry_count: int = 0  # Number of retries on failure
    enabled: bool = True  # Whether step is enabled for execution
    
    def __post_init__(self) -> None:
        """Validate step information after initialization."""
        if self.idx < 0:  # Ensure valid step index
            raise ValueError(f"Step index must be non-negative, got: {self.idx}")
        if not self.name.strip():  # Ensure non-empty step name
            raise ValueError("Step name cannot be empty")
        if not self.module.strip():  # Ensure valid module name
            raise ValueError("Step module cannot be empty")
        if not self.function.strip():  # Ensure valid function name
            raise ValueError("Step function cannot be empty")


@dataclass
class ParsedRecipe:
    """Container for complete parsed recipe with validation results."""
    
    metadata: RecipeMetadata  # Recipe metadata information
    steps: List[StepInfo]  # Parsed and validated steps
    validation_messages: List[ValidationMessage] = field(default_factory=list)  # Validation results
    raw_data: Dict[str, Any] = field(default_factory=dict)  # Original recipe data
    file_path: Optional[str] = None  # Source file path
    file_hash: Optional[str] = None  # Content hash for change detection
    
    @property
    def is_valid(self) -> bool:
        """Check if recipe has no validation errors."""
        return not any(msg.severity == ValidationSeverity.ERROR 
                      for msg in self.validation_messages)
    
    @property
    def error_count(self) -> int:
        """Count of validation errors."""
        return sum(1 for msg in self.validation_messages 
                  if msg.severity == ValidationSeverity.ERROR)
    
    @property
    def warning_count(self) -> int:
        """Count of validation warnings."""
        return sum(1 for msg in self.validation_messages 
                  if msg.severity == ValidationSeverity.WARNING)


class RecipeValidator:
    """Advanced recipe validation with extensible rule system."""
    
    def __init__(self, context: Optional[Context] = None) -> None:
        """
        Initialize recipe validator with optional Context integration.
        
        :param context: Optional Context instance for logging and data sharing
        """
        self.context = context  # Context instance for integration
        self.custom_validators: Dict[str, Callable[[Dict[str, Any]], List[ValidationMessage]]] = {}  # Custom validation functions
        self._setup_default_validators()  # Initialize built-in validators
        
        logger.debug("Recipe validator initialized with Context integration")
    
    def _setup_default_validators(self) -> None:
        """Set up default validation rules for recipe structure."""
        self.custom_validators.update({
            "required_fields": self._validate_required_fields,
            "step_structure": self._validate_step_structure, 
            "dependency_graph": self._validate_dependency_graph,
            "module_imports": self._validate_module_imports,
            "step_indices": self._validate_step_indices
        })
        
        logger.debug("Default validation rules initialized")
    
    def add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None:
        """
        Add custom validation rule to validator.
        
        :param name: Validator name/identifier
        :param validator: Validation function returning ValidationMessage list
        """
        self.custom_validators[name] = validator  # Register custom validator
        logger.debug(f"Custom validator '{name}' registered")
    
    def validate(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]:
        """
        Validate recipe data using all registered validation rules.
        
        :param recipe_data: Raw recipe dictionary to validate
        :return: List of validation messages (errors, warnings, info)
        """
        messages: List[ValidationMessage] = []  # Collect validation messages
        
        logger.debug("Starting comprehensive recipe validation")
        
        # Run all registered validators
        for validator_name, validator_func in self.custom_validators.items():
            try:
                validator_messages = validator_func(recipe_data)  # Execute validator
                messages.extend(validator_messages)  # Collect results
                logger.debug(f"Validator '{validator_name}' completed: {len(validator_messages)} messages")
            except Exception as e:
                # Handle validator exceptions gracefully
                error_msg = ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message=f"Validator '{validator_name}' failed: {str(e)}",
                    location="validator",
                    code="VALIDATOR_ERROR"
                )
                messages.append(error_msg)
                logger.error(f"Validator '{validator_name}' failed with exception: {e}")
        
        # Log validation summary
        error_count = sum(1 for msg in messages if msg.severity == ValidationSeverity.ERROR)
        warning_count = sum(1 for msg in messages if msg.severity == ValidationSeverity.WARNING)
        logger.info(f"Validation completed: {error_count} errors, {warning_count} warnings")
        
        return messages
    
    def _validate_required_fields(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate presence of required recipe fields."""
        messages: List[ValidationMessage] = []
        
        # Check top-level required fields
        required_fields = ["steps"]
        for field in required_fields:
            if field not in recipe_data:
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message=f"Required field '{field}' is missing",
                    location="recipe.root",
                    code="MISSING_FIELD"
                ))
        
        # Validate steps list structure
        if "steps" in recipe_data:
            if not isinstance(recipe_data["steps"], list):
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message="Field 'steps' must be a list",
                    location="recipe.steps",
                    code="INVALID_TYPE"
                ))
            elif len(recipe_data["steps"]) == 0:
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.WARNING,
                    message="Recipe contains no steps",
                    location="recipe.steps",
                    code="EMPTY_STEPS"
                ))
        
        return messages
    
    def _validate_step_structure(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate individual step structure and required fields."""
        messages: List[ValidationMessage] = []
        
        if "steps" not in recipe_data or not isinstance(recipe_data["steps"], list):
            return messages  # Skip if no valid steps list
        
        # Required fields for each step
        required_step_fields = ["name", "module", "function"]
        
        for step_idx, step in enumerate(recipe_data["steps"]):
            step_location = f"recipe.steps[{step_idx}]"
            
            # Validate step is dictionary
            if not isinstance(step, dict):
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message="Step must be a dictionary",
                    location=step_location,
                    code="INVALID_STEP_TYPE"
                ))
                continue
            
            # Check required fields in step
            for field in required_step_fields:
                if field not in step:
                    messages.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"Step missing required field '{field}'",
                        location=f"{step_location}.{field}",
                        code="MISSING_STEP_FIELD"
                    ))
                elif not isinstance(step[field], str) or not step[field].strip():
                    messages.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"Step field '{field}' must be a non-empty string",
                        location=f"{step_location}.{field}",
                        code="INVALID_FIELD_VALUE"
                    ))
        
        return messages
    
    def _validate_dependency_graph(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate step dependency graph for cycles and missing dependencies."""
        messages: List[ValidationMessage] = []
        
        if "steps" not in recipe_data or not isinstance(recipe_data["steps"], list):
            return messages  # Skip if no valid steps list
        
        # Build step name map and dependency graph
        step_names: Set[str] = set()
        dependencies: Dict[str, List[str]] = {}
        
        for step_idx, step in enumerate(recipe_data["steps"]):
            if not isinstance(step, dict) or "name" not in step:
                continue  # Skip invalid steps
            
            step_name = step["name"]
            step_location = f"recipe.steps[{step_idx}]"
            
            # Check for duplicate step names
            if step_name in step_names:
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message=f"Duplicate step name '{step_name}'",
                    location=f"{step_location}.name",
                    code="DUPLICATE_STEP_NAME"
                ))
            else:
                step_names.add(step_name)
            
            # Extract step dependencies
            step_deps = step.get("depends_on", [])
            if isinstance(step_deps, list):
                dependencies[step_name] = step_deps
            else:
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.WARNING,
                    message="Step 'depends_on' should be a list",
                    location=f"{step_location}.depends_on",
                    code="INVALID_DEPENDENCIES"
                ))
        
        # Validate dependency references
        for step_name, step_deps in dependencies.items():
            for dep in step_deps:
                if dep not in step_names:
                    messages.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"Step '{step_name}' depends on non-existent step '{dep}'",
                        location=f"recipe.dependencies",
                        code="MISSING_DEPENDENCY"
                    ))
        
        # Check for circular dependencies using DFS
        visited: Set[str] = set()
        recursion_stack: Set[str] = set()
        
        def has_cycle(node: str) -> bool:
            """Detect cycles in dependency graph using DFS."""
            if node in recursion_stack:
                return True  # Cycle detected
            if node in visited:
                return False  # Already processed
            
            visited.add(node)
            recursion_stack.add(node)
            
            # Visit all dependencies
            for dep in dependencies.get(node, []):
                if has_cycle(dep):
                    return True
            
            recursion_stack.remove(node)
            return False
        
        # Check each step for cycles
        for step_name in step_names:
            if step_name not in visited and has_cycle(step_name):
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message=f"Circular dependency detected involving step '{step_name}'",
                    location="recipe.dependencies",
                    code="CIRCULAR_DEPENDENCY"
                ))
                break  # Stop after finding first cycle
        
        return messages
    
    def _validate_module_imports(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate that required modules and functions can be imported."""
        messages: List[ValidationMessage] = []
        
        if "steps" not in recipe_data or not isinstance(recipe_data["steps"], list):
            return messages  # Skip if no valid steps list
        
        for step_idx, step in enumerate(recipe_data["steps"]):
            if not isinstance(step, dict):
                continue  # Skip invalid steps
            
            step_location = f"recipe.steps[{step_idx}]"
            
            # Extract module and function information
            module_name = step.get("module", "")
            function_name = step.get("function", "")
            
            if not module_name or not function_name:
                continue  # Skip if missing required info
            
            # Attempt to import module and verify function exists
            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, function_name):
                    messages.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"Function '{function_name}' not found in module '{module_name}'",
                        location=f"{step_location}.function",
                        code="MISSING_FUNCTION"
                    ))
            except ModuleNotFoundError:
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.ERROR,
                    message=f"Module '{module_name}' not found",
                    location=f"{step_location}.module",
                    code="MISSING_MODULE"
                ))
            except Exception as e:
                messages.append(ValidationMessage(
                    severity=ValidationSeverity.WARNING,
                    message=f"Could not verify module '{module_name}': {str(e)}",
                    location=f"{step_location}.module",
                    code="MODULE_VERIFICATION_FAILED"
                ))
        
        return messages
    
    def _validate_step_indices(self, recipe_data: Dict[str, Any]) -> List[ValidationMessage]:
        """Validate step index uniqueness and ordering."""
        messages: List[ValidationMessage] = []
        
        if "steps" not in recipe_data or not isinstance(recipe_data["steps"], list):
            return messages  # Skip if no valid steps list
        
        indices: Dict[int, str] = {}  # Map indices to step names
        
        for step_idx, step in enumerate(recipe_data["steps"]):
            if not isinstance(step, dict):
                continue  # Skip invalid steps
            
            step_location = f"recipe.steps[{step_idx}]"
            
            # Check if step has index field
            if "idx" in step:
                idx_value = step["idx"]
                step_name = step.get("name", f"step_{step_idx}")
                
                # Validate index type
                if not isinstance(idx_value, int):
                    messages.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"Step index must be an integer, got: {type(idx_value).__name__}",
                        location=f"{step_location}.idx",
                        code="INVALID_INDEX_TYPE"
                    ))
                    continue
                
                # Check for negative indices
                if idx_value < 0:
                    messages.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"Step index must be non-negative, got: {idx_value}",
                        location=f"{step_location}.idx",
                        code="NEGATIVE_INDEX"
                    ))
                    continue
                
                # Check for duplicate indices
                if idx_value in indices:
                    messages.append(ValidationMessage(
                        severity=ValidationSeverity.ERROR,
                        message=f"Duplicate step index {idx_value} (steps: '{indices[idx_value]}', '{step_name}')",
                        location=f"{step_location}.idx",
                        code="DUPLICATE_INDEX"
                    ))
                else:
                    indices[idx_value] = step_name
        
        return messages


class EnhancedRecipeParser:
    """
    Advanced recipe parser with Context integration and comprehensive features.
    
    This parser provides enhanced functionality over the basic recipe_parser including:
    - Context system integration for logging and data sharing
    - Support for multiple file formats (YAML, JSON)
    - Comprehensive schema validation with detailed error reporting
    - Caching and performance optimization
    - Extensible validation and parsing pipeline
    """
    
    def __init__(self, context: Optional[Context] = None) -> None:
        """
        Initialize enhanced recipe parser with Context integration.
        
        :param context: Optional Context instance for logging and data sharing
        """
        self.context = context or Context()  # Use provided Context or create new one
        self.validator = RecipeValidator(self.context)  # Initialize validator with Context
        self._cache: Dict[str, Tuple[str, ParsedRecipe]] = {}  # Recipe cache (hash -> recipe)
        
        logger.info("Enhanced Recipe Parser initialized with Context integration")
        
        # Record initialization in Context
        if self.context:
            self.context.set("recipe_parser.initialized", True, "enhanced_recipe_parser")
            self.context.set("recipe_parser.init_time", datetime.now().isoformat(), "enhanced_recipe_parser")
    
    def detect_format(self, file_path: str) -> RecipeFormat:
        """
        Detect recipe file format based on file extension.
        
        :param file_path: Path to recipe file
        :return: Detected file format
        :raises ValueError: If file format is not supported
        """
        file_extension = Path(file_path).suffix.lower().lstrip('.')  # Extract extension
        
        # Map extensions to formats
        format_map = {
            'yaml': RecipeFormat.YAML,
            'yml': RecipeFormat.YML, 
            'json': RecipeFormat.JSON
        }
        
        if file_extension not in format_map:
            raise ValueError(f"Unsupported file format: {file_extension}. "
                           f"Supported formats: {list(format_map.keys())}")
        
        detected_format = format_map[file_extension]
        logger.debug(f"Detected format '{detected_format.value}' for file: {file_path}")
        
        return detected_format
    
    def load_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load and parse recipe file content based on detected format.
        
        :param file_path: Path to recipe file
        :return: Parsed recipe data as dictionary
        :raises FileNotFoundError: If file does not exist
        :raises ValueError: If file cannot be parsed
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Recipe file not found: {file_path}")
        
        file_format = self.detect_format(file_path)  # Detect file format
        
        logger.debug(f"Loading recipe file: {file_path} (format: {file_format.value})")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Parse content based on format
            if file_format in [RecipeFormat.YAML, RecipeFormat.YML]:
                data = yaml.safe_load(content)
            elif file_format == RecipeFormat.JSON:
                data = json.loads(content)
            else:
                raise ValueError(f"Unsupported format: {file_format}")
            
            logger.debug(f"Successfully loaded recipe file: {file_path}")
            
            # Record file loading in Context
            if self.context:
                self.context.set(
                    f"recipe_parser.loaded_files.{Path(file_path).stem}",
                    {
                        "path": file_path,
                        "format": file_format.value,
                        "loaded_at": datetime.now().isoformat(),
                        "size": len(content)
                    },
                    "enhanced_recipe_parser"
                )
            
            return data
            
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file '{file_path}': {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON file '{file_path}': {e}")
        except Exception as e:
            raise ValueError(f"Error loading file '{file_path}': {e}")
    
    def _compute_content_hash(self, content: Dict[str, Any]) -> str:
        """
        Compute hash of recipe content for caching and change detection.
        
        :param content: Recipe content dictionary
        :return: SHA-256 hash of content
        """
        content_str = json.dumps(content, sort_keys=True, separators=(',', ':'))  # Normalize content
        return hashlib.sha256(content_str.encode('utf-8')).hexdigest()  # Compute hash
    
    def _extract_metadata(self, recipe_data: Dict[str, Any]) -> RecipeMetadata:
        """
        Extract recipe metadata from raw recipe data.
        
        :param recipe_data: Raw recipe dictionary
        :return: Extracted metadata information
        """
        metadata_section = recipe_data.get("metadata", {})  # Extract metadata section
        
        # Parse timestamps if present
        created = None
        modified = None
        
        if "created" in metadata_section:
            try:
                created = datetime.fromisoformat(str(metadata_section["created"]))
            except ValueError:
                logger.warning(f"Invalid 'created' timestamp format: {metadata_section['created']}")
        
        if "modified" in metadata_section:
            try:
                modified = datetime.fromisoformat(str(metadata_section["modified"]))
            except ValueError:
                logger.warning(f"Invalid 'modified' timestamp format: {metadata_section['modified']}")
        
        # Build metadata object
        metadata = RecipeMetadata(
            name=metadata_section.get("name", "unnamed"),
            version=str(metadata_section.get("version", "1.0")),
            description=str(metadata_section.get("description", "")),
            author=str(metadata_section.get("author", "")),
            created=created,
            modified=modified,
            tags=metadata_section.get("tags", []) if isinstance(metadata_section.get("tags"), list) else [],
            requirements=metadata_section.get("requirements", []) if isinstance(metadata_section.get("requirements"), list) else []
        )
        
        logger.debug(f"Extracted metadata: name='{metadata.name}', version='{metadata.version}'")
        
        return metadata
    
    def _parse_steps(self, recipe_data: Dict[str, Any]) -> List[StepInfo]:
        """
        Parse and validate individual steps from recipe data.
        
        :param recipe_data: Raw recipe dictionary containing steps
        :return: List of parsed step information
        :raises ValueError: If step parsing fails
        """
        if "steps" not in recipe_data:
            return []  # Return empty list if no steps
        
        steps_data = recipe_data["steps"]
        if not isinstance(steps_data, list):
            raise ValueError("Recipe 'steps' must be a list")
        
        parsed_steps: List[StepInfo] = []
        
        for step_idx, step_data in enumerate(steps_data):
            if not isinstance(step_data, dict):
                raise ValueError(f"Step {step_idx} must be a dictionary")
            
            try:
                # Check for required fields before parsing
                required_fields = ["name", "module", "function"]
                missing_fields = [field for field in required_fields if field not in step_data]
                
                if missing_fields:
                    # For invalid steps, create placeholder with validation errors
                    # The validation system will catch and report these issues
                    logger.warning(f"Step {step_idx} missing required fields: {missing_fields}")
                    continue  # Skip invalid steps, let validation handle errors
                
                # Extract step information with defaults
                step_info = StepInfo(
                    name=str(step_data["name"]),
                    idx=int(step_data.get("idx", step_idx)),
                    step_type=str(step_data.get("type", "python")),
                    module=str(step_data["module"]),
                    function=str(step_data["function"]),
                    args=step_data.get("args", {}),
                    depends_on=step_data.get("depends_on", []) if isinstance(step_data.get("depends_on"), list) else [],
                    success_criteria=step_data.get("success", {}),
                    timeout=float(step_data["timeout"]) if "timeout" in step_data else None,
                    retry_count=int(step_data.get("retry_count", 0)),
                    enabled=bool(step_data.get("enabled", True))
                )
                
                parsed_steps.append(step_info)
                logger.debug(f"Parsed step {step_idx}: '{step_info.name}' (idx: {step_info.idx})")
                
            except (KeyError, ValueError, TypeError) as e:
                logger.warning(f"Error parsing step {step_idx}, skipping: {e}")
                continue  # Skip problematic steps, let validation handle errors
        
        # Sort steps by index for execution order
        parsed_steps.sort(key=lambda s: s.idx)
        
        logger.debug(f"Successfully parsed {len(parsed_steps)} valid steps")
        
        return parsed_steps
    
    def parse_recipe(self, file_path: str, use_cache: bool = True) -> ParsedRecipe:
        """
        Parse recipe file with comprehensive validation and Context integration.
        
        :param file_path: Path to recipe file to parse
        :param use_cache: Whether to use cached results if available
        :return: Parsed recipe with validation results
        :raises FileNotFoundError: If recipe file not found
        :raises ValueError: If recipe parsing fails
        """
        logger.info(f"Parsing recipe file: {file_path}")
        
        # Load raw recipe data
        recipe_data = self.load_file(file_path)
        content_hash = self._compute_content_hash(recipe_data)
        
        # Check cache if requested
        if use_cache and file_path in self._cache:
            cached_hash, cached_recipe = self._cache[file_path]
            if cached_hash == content_hash:
                logger.debug(f"Using cached recipe for: {file_path}")
                return cached_recipe
        
        # Parse recipe components
        metadata = self._extract_metadata(recipe_data)
        steps = self._parse_steps(recipe_data)
        
        # Validate recipe
        validation_messages = self.validator.validate(recipe_data)
        
        # Create parsed recipe object
        parsed_recipe = ParsedRecipe(
            metadata=metadata,
            steps=steps,
            validation_messages=validation_messages,
            raw_data=recipe_data,
            file_path=file_path,
            file_hash=content_hash
        )
        
        # Cache result
        if use_cache:
            self._cache[file_path] = (content_hash, parsed_recipe)
        
        # Record parsing results in Context
        if self.context:
            self.context.set(
                f"recipe_parser.parsed.{metadata.name}",
                {
                    "file_path": file_path,
                    "is_valid": parsed_recipe.is_valid,
                    "error_count": parsed_recipe.error_count,
                    "warning_count": parsed_recipe.warning_count,
                    "step_count": len(parsed_recipe.steps),
                    "parsed_at": datetime.now().isoformat()
                },
                "enhanced_recipe_parser"
            )
        
        # Log parsing summary
        logger.info(f"Recipe parsing completed: {parsed_recipe.error_count} errors, "
                   f"{parsed_recipe.warning_count} warnings, {len(parsed_recipe.steps)} steps")
        
        return parsed_recipe
    
    def get_validation_summary(self, parsed_recipe: ParsedRecipe) -> str:
        """
        Generate human-readable validation summary for parsed recipe.
        
        :param parsed_recipe: Parsed recipe with validation results
        :return: Formatted validation summary string
        """
        lines = [
            f"Recipe Validation Summary for '{parsed_recipe.metadata.name}':",
            f"  File: {parsed_recipe.file_path or 'N/A'}",
            f"  Status: {'VALID' if parsed_recipe.is_valid else 'INVALID'}",
            f"  Errors: {parsed_recipe.error_count}",
            f"  Warnings: {parsed_recipe.warning_count}",
            f"  Steps: {len(parsed_recipe.steps)}"
        ]
        
        # Add detailed messages if present
        if parsed_recipe.validation_messages:
            lines.append("\nValidation Messages:")
            for msg in parsed_recipe.validation_messages:
                lines.append(f"  {msg}")
        
        return "\n".join(lines)
    
    def clear_cache(self) -> None:
        """Clear internal recipe cache."""
        self._cache.clear()
        logger.debug("Recipe parser cache cleared")
    
    def add_validator(self, name: str, validator: Callable[[Dict[str, Any]], List[ValidationMessage]]) -> None:
        """
        Add custom validation rule to parser.
        
        :param name: Validator name/identifier
        :param validator: Validation function returning ValidationMessage list
        """
        self.validator.add_validator(name, validator)
        logger.debug(f"Custom validator '{name}' added to parser")


def parse_recipe_file(file_path: str, context: Optional[Context] = None) -> ParsedRecipe:
    """
    Convenience function for parsing recipe files with Context integration.
    
    This function provides backward compatibility with the existing recipe_parser
    interface while leveraging the enhanced features of EnhancedRecipeParser.
    
    :param file_path: Path to recipe file to parse
    :param context: Optional Context instance for integration
    :return: Parsed recipe with validation results
    :raises FileNotFoundError: If recipe file not found
    :raises ValueError: If recipe parsing fails
    """
    parser = EnhancedRecipeParser(context)  # Create parser instance
    return parser.parse_recipe(file_path)  # Parse and return recipe


def validate_recipe_data(recipe_data: Dict[str, Any], context: Optional[Context] = None) -> List[ValidationMessage]:
    """
    Convenience function for validating recipe data with Context integration.
    
    :param recipe_data: Raw recipe dictionary to validate
    :param context: Optional Context instance for integration
    :return: List of validation messages
    """
    validator = RecipeValidator(context)  # Create validator instance
    return validator.validate(recipe_data)  # Validate and return messages


# Backward compatibility aliases
load_recipe = lambda file_path: EnhancedRecipeParser().load_file(file_path)
validate_recipe = lambda recipe: validate_recipe_data(recipe)
parse_step = lambda step: StepInfo(**step) if isinstance(step, dict) else None