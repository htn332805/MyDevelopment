# src/templates/scriptlet_templates.py

"""
Template system for creating standardized scriptlets in Framework0.

This module provides templates and generators for creating consistent,
well-structured scriptlets with proper monitoring, error handling,
and documentation. Includes templates for common patterns and use cases.
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass
from string import Template

# Import Framework0 components
from src.core.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


@dataclass
class ScriptletTemplate:
    """Template definition for generating scriptlets."""
    name: str  # Template name
    description: str  # Template description
    category: str  # Template category
    template_content: str  # Template file content
    required_params: List[str]  # Required template parameters
    optional_params: Dict[str, Any]  # Optional parameters with defaults


class ScriptletTemplateGenerator:
    """
    Generator for creating scriptlets from templates.
    
    Provides standardized scriptlet generation with proper structure,
    documentation, and Framework0 integration patterns.
    """

    def __init__(self: 'ScriptletTemplateGenerator') -> None:
        # Initialize template generator with built-in templates
        """Initialize template generator."""
        self.templates: Dict[str, ScriptletTemplate] = {}
        self._load_builtin_templates()
        
        logger.info("ScriptletTemplateGenerator initialized")

    def _load_builtin_templates(self: 'ScriptletTemplateGenerator') -> None:
        # Load built-in scriptlet templates for common patterns
        """Load built-in scriptlet templates."""
        
        # Basic scriptlet template
        basic_template = ScriptletTemplate(
            name="basic_scriptlet",
            description="Basic scriptlet with monitoring and error handling",
            category="general",
            template_content=self._get_basic_scriptlet_template(),
            required_params=["class_name", "description"],
            optional_params={
                "author": "Framework0 Developer",
                "version": "1.0.0",
                "enable_monitoring": True,
                "enable_debugging": False,
                "validation_rules": {}
            }
        )
        self.templates["basic_scriptlet"] = basic_template
        
        logger.debug(f"Loaded {len(self.templates)} built-in templates")

    def _get_basic_scriptlet_template(self: 'ScriptletTemplateGenerator') -> str:
        # Get basic scriptlet template content with Framework0 patterns
        """Get basic scriptlet template content."""
        return '''# ${filename}

"""
${description}

This scriptlet provides ${functionality} with comprehensive monitoring,
error handling, and Framework0 integration.

Author: ${author}
Version: ${version}
"""

from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import time

# Framework0 imports
from src.core.logger import get_logger
from src.core.context_v2 import ContextV2
from scriptlets.core.base_v2 import BaseScriptletV2, ScriptletResult, ScriptletConfig


class ${class_name}(BaseScriptletV2):
    """
    ${description}
    
    This scriptlet implements ${functionality} with proper validation,
    monitoring, and error handling according to Framework0 patterns.
    """

    def validate_custom(self, context: ContextV2, params: Dict[str, Any]) -> bool:
        # Custom validation logic for scriptlet with parameter checking
        """
        Custom validation logic for ${class_name}.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Parameters to validate
            
        Returns:
            bool: True if validation passes
        """
        # Add custom validation logic here
        ${validation_logic}
        
        return True

    def execute(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        # Execute scriptlet with comprehensive monitoring and error handling  
        """
        Execute ${class_name} with comprehensive monitoring.
        
        Args:
            context (ContextV2): Execution context
            params (Dict[str, Any]): Execution parameters
            
        Returns:
            ScriptletResult: Execution result
        """
        try:
            self.logger.info(f"Starting ${class_name} execution")
            
            # Extract parameters
            ${parameter_extraction}
            
            # Perform main operation
            result_data = self._perform_operation(params)
            
            # Store results in context if needed
            output_key = params.get("output_key", "${default_output_key}")
            if output_key:
                context.set(output_key, result_data, who=self.name)
            
            self.logger.info(f"${class_name} completed successfully")
            
            return ScriptletResult(
                success=True,
                exit_code=0,
                message="${class_name} execution completed successfully",
                data=result_data
            )
            
        except Exception as e:
            self.logger.error(f"${class_name} execution failed: {e}")
            return ScriptletResult(
                success=False,
                exit_code=1,
                message=f"${class_name} execution failed: {str(e)}",
                error_details=str(e)
            )

    def _perform_operation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Perform the main operation logic with parameter processing
        """
        Perform the main operation logic.
        
        Args:
            params (Dict[str, Any]): Operation parameters
            
        Returns:
            Dict[str, Any]: Operation results
        """
        # Implement main operation logic here
        ${operation_logic}
        
        return {"status": "completed", "timestamp": time.time()}


# Factory function for creating scriptlet instances
def create_${class_name_lower}(**config_kwargs) -> ${class_name}:
    # Create scriptlet instance with configuration parameters
    """Create ${class_name} instance with configuration."""
    config = ScriptletConfig(
        enable_monitoring=${enable_monitoring},
        enable_debugging=${enable_debugging},
        **config_kwargs
    )
    return ${class_name}(config=config)
'''

    def list_templates(self: 'ScriptletTemplateGenerator') -> List[Dict[str, Any]]:
        # List available templates with metadata and descriptions
        """
        List available templates.
        
        Returns:
            List[Dict[str, Any]]: Template information
        """
        return [
            {
                "name": template.name,
                "description": template.description,
                "category": template.category,
                "required_params": template.required_params,
                "optional_params": list(template.optional_params.keys())
            }
            for template in self.templates.values()
        ]

    def generate_scriptlet(self: 'ScriptletTemplateGenerator', template_name: str, output_path: str, **template_params) -> bool:
        # Generate scriptlet from template with parameter substitution
        """
        Generate scriptlet from template.
        
        Args:
            template_name (str): Template to use
            output_path (str): Output file path
            **template_params: Template parameters
            
        Returns:
            bool: True if generation successful
        """
        if template_name not in self.templates:
            logger.error(f"Template not found: {template_name}")
            return False
        
        template = self.templates[template_name]
        
        # Check required parameters
        missing_params = set(template.required_params) - set(template_params.keys())
        if missing_params:
            logger.error(f"Missing required parameters: {missing_params}")
            return False
        
        # Merge parameters with defaults
        all_params = {**template.optional_params, **template_params}
        
        # Add derived parameters
        all_params.update(self._generate_derived_params(template_name, all_params))
        
        try:
            # Generate content from template
            template_obj = Template(template.template_content)
            generated_content = template_obj.safe_substitute(all_params)
            
            # Write to output file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                f.write(generated_content)
            
            logger.info(f"Generated {template_name} to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate {template_name}: {e}")
            return False

    def _generate_derived_params(self: 'ScriptletTemplateGenerator', template_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        # Generate derived parameters from base parameters for template processing  
        """Generate derived parameters from base parameters."""
        derived = {}
        
        # Common derived parameters
        if "class_name" in params:
            derived["class_name_lower"] = params["class_name"].lower()
            derived["filename"] = f"{params['class_name'].lower()}.py"
        
        # Template-specific derived parameters
        if template_name == "basic_scriptlet":
            derived.update({
                "functionality": "basic operations",
                "default_output_key": "basic_result", 
                "validation_logic": "# Add validation logic here",
                "parameter_extraction": "# Extract required parameters",
                "operation_logic": "# Implement operation logic here"
            })
        
        return derived


# Global template generator instance
_generator: Optional[ScriptletTemplateGenerator] = None


def get_template_generator() -> ScriptletTemplateGenerator:
    # Get global template generator instance using singleton pattern
    """Get global template generator instance."""
    global _generator
    
    if _generator is None:
        _generator = ScriptletTemplateGenerator()
    
    return _generator


def generate_scriptlet(template_name: str, output_path: str, **params) -> bool:
    # Generate scriptlet using global template generator with parameters
    """Generate scriptlet using global template generator."""
    return get_template_generator().generate_scriptlet(template_name, output_path, **params)


def list_available_templates() -> List[Dict[str, Any]]:
    # List available templates using global generator instance
    """List available templates using global generator."""
    return get_template_generator().list_templates()