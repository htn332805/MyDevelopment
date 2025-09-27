# plugins/examples/data_processing_plugin.py

"""
Example data processing plugin demonstrating Framework0 plugin capabilities.

This plugin provides data processing capabilities including:
- CSV data loading and processing
- Data validation and cleaning
- Statistical analysis and reporting
- Data transformation and export

Demonstrates plugin metadata, lifecycle management, and Framework0 integration.
"""

import pandas as pd
import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

# Framework0 imports
from src.core.plugin_registry import BasePlugin
from src.core.logger import get_logger
from src.core.context_v2 import ContextV2
from scriptlets.core.base_v2 import BaseScriptletV2, ScriptletResult, ScriptletConfig

# Plugin metadata for automatic discovery
__plugin_metadata__ = {
    "name": "DataProcessingPlugin",
    "version": "1.0.0",
    "author": "Framework0 Team",
    "description": "Advanced data processing capabilities with CSV support, validation, and analysis",
    "entry_point": "data_processing_plugin:DataProcessingPlugin",
    "dependencies": [],
    "framework_version": ">=0.1.0",
    "category": "data",
    "tags": ["csv", "data", "analysis", "processing"],
    "config_schema": {
        "default_encoding": {"type": "string", "default": "utf-8"},
        "max_rows": {"type": "integer", "default": 10000},
        "enable_validation": {"type": "boolean", "default": True}
    },
    "permissions": ["read_files", "write_files"],
    "hot_reload": True
}


class CSVProcessorScriptlet(BaseScriptletV2):
    """
    Scriptlet for processing CSV files with validation and analysis.
    
    Provides comprehensive CSV processing capabilities including loading,
    validation, cleaning, and statistical analysis.
    """

    def validate_custom(self, context: ContextV2, params: Dict[str, Any]) -> bool:
        """Validate CSV processor parameters."""
        # Check required parameters
        if "file_path" not in params:
            self.logger.error("Missing required parameter: file_path")
            return False
        
        file_path = Path(params["file_path"])
        if not file_path.exists():
            self.logger.error(f"CSV file does not exist: {file_path}")
            return False
        
        if not file_path.suffix.lower() == ".csv":
            self.logger.error(f"File is not a CSV file: {file_path}")
            return False
        
        return True

    def execute(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        """Execute CSV processing with comprehensive analysis."""
        try:
            file_path = params["file_path"]
            encoding = params.get("encoding", "utf-8")
            max_rows = params.get("max_rows", 10000)
            
            self.logger.info(f"Processing CSV file: {file_path}")
            
            # Load CSV data
            df = pd.read_csv(file_path, encoding=encoding, nrows=max_rows)
            
            # Basic data info
            data_info = {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum()
            }
            
            # Data quality analysis
            quality_info = {
                "missing_values": df.isnull().sum().to_dict(),
                "duplicate_rows": df.duplicated().sum(),
                "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
                "categorical_columns": df.select_dtypes(include=['object']).columns.tolist()
            }
            
            # Statistical summary for numeric columns
            stats_summary = {}
            if quality_info["numeric_columns"]:
                stats = df[quality_info["numeric_columns"]].describe()
                stats_summary = stats.to_dict()
            
            # Store results in context
            output_key = params.get("output_key", "csv_analysis")
            context.set(f"{output_key}.data_info", data_info, who=self.name)
            context.set(f"{output_key}.quality_info", quality_info, who=self.name)
            context.set(f"{output_key}.statistics", stats_summary, who=self.name)
            
            # Store processed data if requested
            if params.get("store_data", False):
                context.set(f"{output_key}.data", df.to_dict('records'), who=self.name)
            
            self.logger.info(f"CSV processing completed: {data_info['rows']} rows, "
                           f"{data_info['columns']} columns")
            
            return ScriptletResult(
                success=True,
                exit_code=0,
                message=f"Successfully processed CSV file with {data_info['rows']} rows",
                data={
                    "file_path": str(file_path),
                    "data_info": data_info,
                    "quality_info": quality_info,
                    "statistics": stats_summary
                }
            )
            
        except Exception as e:
            self.logger.error(f"CSV processing failed: {e}")
            return ScriptletResult(
                success=False,
                exit_code=1,
                message=f"CSV processing failed: {str(e)}",
                error_details=str(e)
            )


class DataValidatorScriptlet(BaseScriptletV2):
    """
    Scriptlet for validating data against defined schemas and rules.
    
    Provides comprehensive data validation with customizable rules
    and detailed reporting of validation results.
    """

    def execute(self, context: ContextV2, params: Dict[str, Any]) -> ScriptletResult:
        """Execute data validation with comprehensive rule checking."""
        try:
            data_key = params.get("data_key", "csv_analysis.data")
            validation_rules = params.get("validation_rules", {})
            
            # Get data from context
            data = context.get(data_key)
            if data is None:
                return ScriptletResult(
                    success=False,
                    exit_code=1,
                    message=f"No data found at key: {data_key}"
                )
            
            # Convert to DataFrame if list of dicts
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                df = pd.DataFrame(data)
            else:
                self.logger.error("Data format not supported for validation")
                return ScriptletResult(
                    success=False,
                    exit_code=1,
                    message="Data format not supported for validation"
                )
            
            # Validation results
            validation_results = {
                "total_rows": len(df),
                "validation_passed": True,
                "errors": [],
                "warnings": []
            }
            
            # Apply validation rules
            for rule_name, rule_config in validation_rules.items():
                try:
                    if rule_name == "required_columns":
                        missing_cols = set(rule_config) - set(df.columns)
                        if missing_cols:
                            validation_results["errors"].append({
                                "rule": "required_columns",
                                "message": f"Missing required columns: {list(missing_cols)}"
                            })
                            validation_results["validation_passed"] = False
                    
                    elif rule_name == "data_types":
                        for col, expected_type in rule_config.items():
                            if col in df.columns:
                                actual_type = str(df[col].dtype)
                                if expected_type not in actual_type:
                                    validation_results["warnings"].append({
                                        "rule": "data_types",
                                        "column": col,
                                        "message": f"Expected {expected_type}, got {actual_type}"
                                    })
                    
                    elif rule_name == "value_ranges":
                        for col, range_config in rule_config.items():
                            if col in df.columns and df[col].dtype.kind in 'bifc':  # numeric
                                min_val = range_config.get("min")
                                max_val = range_config.get("max")
                                
                                if min_val is not None:
                                    violations = (df[col] < min_val).sum()
                                    if violations > 0:
                                        validation_results["errors"].append({
                                            "rule": "value_ranges",
                                            "column": col,
                                            "message": f"{violations} values below minimum {min_val}"
                                        })
                                        validation_results["validation_passed"] = False
                                
                                if max_val is not None:
                                    violations = (df[col] > max_val).sum()
                                    if violations > 0:
                                        validation_results["errors"].append({
                                            "rule": "value_ranges",
                                            "column": col,
                                            "message": f"{violations} values above maximum {max_val}"
                                        })
                                        validation_results["validation_passed"] = False
                    
                except Exception as rule_error:
                    validation_results["errors"].append({
                        "rule": rule_name,
                        "message": f"Rule execution failed: {str(rule_error)}"
                    })
                    validation_results["validation_passed"] = False
            
            # Store validation results
            output_key = params.get("output_key", "data_validation")
            context.set(output_key, validation_results, who=self.name)
            
            self.logger.info(f"Data validation completed: "
                           f"passed={validation_results['validation_passed']}, "
                           f"errors={len(validation_results['errors'])}, "
                           f"warnings={len(validation_results['warnings'])}")
            
            return ScriptletResult(
                success=True,
                exit_code=0 if validation_results["validation_passed"] else 1,
                message=f"Data validation completed with {len(validation_results['errors'])} errors",
                data=validation_results
            )
            
        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            return ScriptletResult(
                success=False,
                exit_code=1,
                message=f"Data validation failed: {str(e)}",
                error_details=str(e)
            )


class DataProcessingPlugin(BasePlugin):
    """
    Advanced data processing plugin with CSV support and validation.
    
    Provides comprehensive data processing capabilities including file loading,
    validation, analysis, and reporting with Framework0 integration.
    """

    def __init__(self):
        """Initialize data processing plugin."""
        super().__init__()
        self._scriptlets: Dict[str, BaseScriptletV2] = {}
        
    def get_capabilities(self) -> List[str]:
        """Return plugin capabilities."""
        return [
            "csv_processing",
            "data_validation", 
            "statistical_analysis",
            "data_quality_reporting",
            "file_operations"
        ]

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration."""
        super().initialize(config)
        
        # Create scriptlet instances
        csv_config = ScriptletConfig(
            parameters={
                "encoding": config.get("default_encoding", "utf-8"),
                "max_rows": config.get("max_rows", 10000)
            },
            enable_monitoring=True,
            enable_debugging=config.get("debug", False)
        )
        
        validator_config = ScriptletConfig(
            enable_monitoring=True,
            enable_debugging=config.get("debug", False)
        )
        
        self._scriptlets["csv_processor"] = CSVProcessorScriptlet(config=csv_config)
        self._scriptlets["data_validator"] = DataValidatorScriptlet(config=validator_config)
        
        self.logger.info("Data processing plugin initialized with CSV and validation support")

    def activate(self) -> None:
        """Activate plugin functionality."""
        super().activate()
        
        # Register scriptlets or capabilities as needed
        self.logger.info("Data processing plugin activated - scriptlets ready for use")

    def process_csv(self, file_path: str, context: ContextV2, **kwargs) -> ScriptletResult:
        """
        Process CSV file using the CSV processor scriptlet.
        
        Args:
            file_path (str): Path to CSV file
            context (ContextV2): Execution context
            **kwargs: Additional processing parameters
            
        Returns:
            ScriptletResult: Processing result
        """
        if not self.is_active:
            raise RuntimeError("Plugin not active")
        
        params = {"file_path": file_path, **kwargs}
        return self._scriptlets["csv_processor"].run(context, params)

    def validate_data(self, context: ContextV2, validation_rules: Dict[str, Any], **kwargs) -> ScriptletResult:
        """
        Validate data using the data validator scriptlet.
        
        Args:
            context (ContextV2): Execution context with data
            validation_rules (Dict[str, Any]): Validation rules to apply
            **kwargs: Additional validation parameters
            
        Returns:
            ScriptletResult: Validation result
        """
        if not self.is_active:
            raise RuntimeError("Plugin not active")
        
        params = {"validation_rules": validation_rules, **kwargs}
        return self._scriptlets["data_validator"].run(context, params)

    def get_scriptlets(self) -> Dict[str, BaseScriptletV2]:
        """Get available scriptlets."""
        return self._scriptlets.copy()

    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        super().cleanup()
        
        # Cleanup scriptlets
        for scriptlet in self._scriptlets.values():
            try:
                scriptlet.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up scriptlet: {e}")
        
        self._scriptlets.clear()
        self.logger.info("Data processing plugin cleaned up")