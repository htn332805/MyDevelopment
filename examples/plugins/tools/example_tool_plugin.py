#!/usr/bin/env python3
"""
Framework0 Example Tool Plugin

Demonstrates IToolPlugin interface implementation with utility functions,
data processing, file operations, and enhanced logging integration.

Author: Framework0 Development Team
Date: 2025-10-05
Version: 1.0.0-example-tool
"""

# import os  # For file and environment operations (not used directly in this example)
import json  # For JSON processing
import csv  # For CSV operations
import hashlib  # For hashing operations
import base64  # For encoding operations
import time  # For timing operations
import re  # For regular expressions
from typing import Dict, Any, List  # Type safety
from pathlib import Path  # For path operations
from dataclasses import dataclass, field  # Structured data classes
import urllib.parse  # For URL operations
import datetime  # For date/time operations

# Import Framework0 plugin interfaces with fallback
try:
    from src.core.plugin_interfaces_v2 import (
        BaseFrameworkPlugin,
        PluginMetadata,
        PluginCapability,
        PluginPriority,
        PluginExecutionContext,
        PluginExecutionResult,
    )
    _HAS_PLUGIN_INTERFACES = True
except ImportError:
    _HAS_PLUGIN_INTERFACES = False
    
    # Fallback definitions for standalone operation
    from enum import Enum
    
    class PluginCapability(Enum):
        """Fallback capability enum."""
        FILE_OPERATIONS = "file_operations"
        DATA_PROCESSING = "data_processing"
        TEXT_PROCESSING = "text_processing"
        UTILITY_FUNCTIONS = "utility_functions"
    
    class PluginPriority(Enum):
        """Fallback priority enum."""
        HIGH = 10
        NORMAL = 50
    
    @dataclass
    class PluginMetadata:
        """Fallback metadata class."""
        plugin_id: str
        name: str
        version: str
        description: str = ""
        author: str = ""
        plugin_type: str = "tool"
        priority: PluginPriority = PluginPriority.NORMAL
    
    @dataclass
    class PluginExecutionContext:
        """Fallback execution context."""
        correlation_id: str = ""
        operation: str = "execute"
        parameters: Dict[str, Any] = field(default_factory=dict)
    
    @dataclass
    class PluginExecutionResult:
        """Fallback execution result."""
        success: bool = True
        result: Any = None
        error: str = ""
        execution_time: float = 0.0
    
    class BaseFrameworkPlugin:
        """Fallback base plugin class."""
        def __init__(self):
            self._logger = None
        
        def initialize(self, context):
            return True
        
        def cleanup(self):
            return True


@dataclass
class FileOperationResult:
    """Result of file operation."""
    
    success: bool  # Operation success status
    file_path: str  # File path involved
    operation: str  # Operation performed
    size_bytes: int = 0  # File size in bytes
    lines_processed: int = 0  # Lines processed (if applicable)
    error_message: str = ""  # Error message if failed
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata


@dataclass
class DataProcessingResult:
    """Result of data processing operation."""
    
    success: bool  # Processing success status
    input_count: int  # Number of input items
    output_count: int  # Number of output items
    processing_time: float  # Processing time in seconds
    statistics: Dict[str, Any] = field(
        default_factory=dict
    )  # Processing statistics
    transformed_data: Any = None  # Processed data
    error_message: str = ""  # Error message if failed


class ExampleToolPlugin(BaseFrameworkPlugin):
    """
    Example Tool Plugin for Framework0.
    
    Demonstrates comprehensive tool capabilities including:
    - File operations (read, write, process)
    - Data processing and transformation
    - Text processing and utilities
    - Encoding/decoding operations
    """
    
    def __init__(self):
        """Initialize the tool plugin."""
        super().__init__()
        
        # Plugin state
        self._operation_history: List[Dict[str, Any]] = []
        self._cached_results: Dict[str, Any] = {}
        self._file_registry: Dict[str, Dict[str, Any]] = {}
        
        # Performance metrics
        self._operations_performed = 0
        self._total_processing_time = 0.0
        self._files_processed = 0
        self._data_items_processed = 0
        
        # Supported operations
        self._supported_operations = {
            # File operations
            "read_file": self._read_file,
            "write_file": self._write_file,
            "process_csv": self._process_csv,
            "process_json": self._process_json,
            
            # Data processing
            "transform_data": self._transform_data,
            "filter_data": self._filter_data,
            "aggregate_data": self._aggregate_data,
            "validate_data": self._validate_data,
            
            # Text processing
            "process_text": self._process_text,
            "extract_patterns": self._extract_patterns,
            "format_text": self._format_text,
            
            # Utility functions
            "hash_data": self._hash_data,
            "encode_data": self._encode_data,
            "decode_data": self._decode_data,
            "generate_id": self._generate_id,
            
            # Status and metadata
            "get_status": self._get_status
        }
        
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata information."""
        return PluginMetadata(
            plugin_id="example_tool_plugin",
            name="Example Tool Plugin",
            version="1.0.0",
            description=("Demonstrates comprehensive tool capabilities "
                        "with file operations and data processing"),
            author="Framework0 Development Team",
            plugin_type="tool",
            priority=PluginPriority.HIGH
        )
        
    def get_capabilities(self) -> List[PluginCapability]:
        """Get list of plugin capabilities."""
        return [
            PluginCapability.FILE_OPERATIONS,
            PluginCapability.DATA_PROCESSING,
            PluginCapability.TEXT_PROCESSING,
            PluginCapability.UTILITY_FUNCTIONS
        ]
        
    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        """Execute plugin functionality based on operation type."""
        start_time = time.time()
        
        try:
            operation = context.operation
            parameters = context.parameters
            
            if self._logger:
                self._logger.info(f"Executing tool operation: {operation}")
            
            # Check if operation is supported
            if operation not in self._supported_operations:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown operation: {operation}. "
                           f"Supported: {list(self._supported_operations.keys())}"
                )
            
            # Execute operation
            operation_func = self._supported_operations[operation]
            result = operation_func(parameters, context)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            self._total_processing_time += execution_time
            self._operations_performed += 1
            
            # Update operation history
            self._update_operation_history(operation, parameters, result)
            
            if self._logger:
                status = "successful" if result.success else "failed"
                self._logger.info(
                    f"Tool operation {operation} {status} "
                    f"(time: {execution_time:.3f}s)"
                )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Tool plugin execution failed: {e}"
            
            if self._logger:
                self._logger.error(error_msg)
            
            return PluginExecutionResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
    
    def _read_file(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Read file operation."""
        try:
            file_path = parameters.get("file_path", "")
            encoding = parameters.get("encoding", "utf-8")
            max_lines = parameters.get("max_lines", -1)
            
            if not file_path:
                return PluginExecutionResult(
                    success=False,
                    error="file_path parameter required"
                )
            
            path_obj = Path(file_path)
            if not path_obj.exists():
                return PluginExecutionResult(
                    success=False,
                    error=f"File not found: {file_path}"
                )
            
            # Read file content
            with open(path_obj, 'r', encoding=encoding) as file:
                if max_lines > 0:
                    lines = []
                    for i, line in enumerate(file):
                        if i >= max_lines:
                            break
                        lines.append(line.rstrip('\n\r'))
                    content = '\n'.join(lines)
                    lines_read = len(lines)
                else:
                    content = file.read()
                    lines_read = content.count('\n') + 1
            
            # Get file statistics
            file_stats = path_obj.stat()
            
            result_data = {
                "content": content,
                "file_size": file_stats.st_size,
                "lines_read": lines_read,
                "encoding": encoding,
                "last_modified": datetime.datetime.fromtimestamp(
                    file_stats.st_mtime
                ).isoformat()
            }
            
            self._files_processed += 1
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except UnicodeDecodeError as e:
            return PluginExecutionResult(
                success=False,
                error=f"Encoding error reading file: {e}"
            )
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"File read error: {e}"
            )
    
    def _write_file(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Write file operation."""
        try:
            file_path = parameters.get("file_path", "")
            content = parameters.get("content", "")
            encoding = parameters.get("encoding", "utf-8")
            append_mode = parameters.get("append", False)
            create_dirs = parameters.get("create_directories", True)
            
            if not file_path:
                return PluginExecutionResult(
                    success=False,
                    error="file_path parameter required"
                )
            
            path_obj = Path(file_path)
            
            # Create parent directories if needed
            if create_dirs and not path_obj.parent.exists():
                path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file content
            mode = 'a' if append_mode else 'w'
            with open(path_obj, mode, encoding=encoding) as file:
                file.write(content)
            
            # Get file statistics
            file_stats = path_obj.stat()
            lines_written = content.count('\n') + (1 if content else 0)
            
            result_data = {
                "file_path": str(path_obj),
                "bytes_written": len(content.encode(encoding)),
                "lines_written": lines_written,
                "file_size": file_stats.st_size,
                "mode": "append" if append_mode else "overwrite"
            }
            
            self._files_processed += 1
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"File write error: {e}"
            )
    
    def _process_csv(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Process CSV file operation."""
        try:
            file_path = parameters.get("file_path", "")
            operation_type = parameters.get("operation", "read")
            delimiter = parameters.get("delimiter", ",")
            has_header = parameters.get("has_header", True)
            max_rows = parameters.get("max_rows", -1)
            
            if not file_path:
                return PluginExecutionResult(
                    success=False,
                    error="file_path parameter required"
                )
            
            path_obj = Path(file_path)
            
            if operation_type == "read":
                if not path_obj.exists():
                    return PluginExecutionResult(
                        success=False,
                        error=f"CSV file not found: {file_path}"
                    )
                
                rows = []
                headers = []
                
                with open(path_obj, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=delimiter)
                    
                    if has_header:
                        headers = next(reader, [])
                    
                    for i, row in enumerate(reader):
                        if max_rows > 0 and i >= max_rows:
                            break
                        
                        if has_header and headers:
                            rows.append(dict(zip(headers, row)))
                        else:
                            rows.append(row)
                
                result_data = {
                    "rows": rows,
                    "headers": headers,
                    "row_count": len(rows),
                    "has_header": has_header,
                    "delimiter": delimiter
                }
                
                self._data_items_processed += len(rows)
                
            elif operation_type == "write":
                data = parameters.get("data", [])
                headers = parameters.get("headers", [])
                
                if not data:
                    return PluginExecutionResult(
                        success=False,
                        error="data parameter required for CSV write"
                    )
                
                with open(path_obj, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=delimiter)
                    
                    if headers:
                        writer.writerow(headers)
                    
                    if isinstance(data[0], dict) and headers:
                        for row in data:
                            writer.writerow([row.get(h, '') for h in headers])
                    else:
                        writer.writerows(data)
                
                result_data = {
                    "file_path": str(path_obj),
                    "rows_written": len(data),
                    "headers_written": len(headers),
                    "delimiter": delimiter
                }
                
                self._data_items_processed += len(data)
            
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown CSV operation: {operation_type}"
                )
            
            self._files_processed += 1
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"CSV processing error: {e}"
            )
    
    def _process_json(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Process JSON file operation."""
        try:
            operation_type = parameters.get("operation", "read")
            
            if operation_type == "read":
                file_path = parameters.get("file_path", "")
                
                if not file_path:
                    return PluginExecutionResult(
                        success=False,
                        error="file_path parameter required"
                    )
                
                path_obj = Path(file_path)
                if not path_obj.exists():
                    return PluginExecutionResult(
                        success=False,
                        error=f"JSON file not found: {file_path}"
                    )
                
                with open(path_obj, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                result_data = {
                    "data": data,
                    "file_path": str(path_obj),
                    "data_type": type(data).__name__,
                    "size_info": self._get_data_size_info(data)
                }
                
            elif operation_type == "write":
                file_path = parameters.get("file_path", "")
                data = parameters.get("data")
                indent = parameters.get("indent", 2)
                
                if not file_path:
                    return PluginExecutionResult(
                        success=False,
                        error="file_path parameter required"
                    )
                
                if data is None:
                    return PluginExecutionResult(
                        success=False,
                        error="data parameter required for JSON write"
                    )
                
                path_obj = Path(file_path)
                
                with open(path_obj, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=indent, ensure_ascii=False)
                
                result_data = {
                    "file_path": str(path_obj),
                    "data_type": type(data).__name__,
                    "indent": indent,
                    "size_info": self._get_data_size_info(data)
                }
                
            elif operation_type == "validate":
                json_string = parameters.get("json_string", "")
                
                if not json_string:
                    return PluginExecutionResult(
                        success=False,
                        error="json_string parameter required"
                    )
                
                try:
                    parsed_data = json.loads(json_string)
                    result_data = {
                        "valid": True,
                        "data": parsed_data,
                        "data_type": type(parsed_data).__name__,
                        "size_info": self._get_data_size_info(parsed_data)
                    }
                except json.JSONDecodeError as e:
                    result_data = {
                        "valid": False,
                        "error": str(e),
                        "line": getattr(e, 'lineno', None),
                        "column": getattr(e, 'colno', None)
                    }
            
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown JSON operation: {operation_type}"
                )
            
            self._files_processed += 1
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"JSON processing error: {e}"
            )
    
    def _transform_data(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Transform data operation."""
        try:
            data = parameters.get("data", [])
            transformation = parameters.get("transformation", "identity")
            transform_params = parameters.get("transform_parameters", {})
            
            if not data:
                return PluginExecutionResult(
                    success=False,
                    error="data parameter required"
                )
            
            transformed_data = []
            
            if transformation == "map":
                # Apply mapping transformation
                mapping_func = transform_params.get("function", "identity")
                field_name = transform_params.get("field")
                
                for item in data:
                    if isinstance(item, dict) and field_name:
                        new_item = item.copy()
                        if mapping_func == "uppercase":
                            new_item[field_name] = str(item.get(field_name, "")).upper()
                        elif mapping_func == "lowercase":
                            new_item[field_name] = str(item.get(field_name, "")).lower()
                        elif mapping_func == "double":
                            try:
                                new_item[field_name] = float(item.get(field_name, 0)) * 2
                            except (ValueError, TypeError):
                                new_item[field_name] = item.get(field_name)
                        transformed_data.append(new_item)
                    else:
                        transformed_data.append(item)
            
            elif transformation == "filter":
                # Apply filter transformation
                filter_field = transform_params.get("field")
                filter_value = transform_params.get("value")
                filter_operator = transform_params.get("operator", "equals")
                
                for item in data:
                    if isinstance(item, dict) and filter_field:
                        item_value = item.get(filter_field)
                        
                        if filter_operator == "equals":
                            if item_value == filter_value:
                                transformed_data.append(item)
                        elif filter_operator == "contains":
                            if filter_value in str(item_value):
                                transformed_data.append(item)
                        elif filter_operator == "greater_than":
                            try:
                                if float(item_value) > float(filter_value):
                                    transformed_data.append(item)
                            except (ValueError, TypeError):
                                pass
                    else:
                        transformed_data.append(item)
            
            elif transformation == "sort":
                # Apply sort transformation
                sort_field = transform_params.get("field")
                reverse = transform_params.get("reverse", False)
                
                if sort_field and isinstance(data[0], dict):
                    transformed_data = sorted(
                        data,
                        key=lambda x: x.get(sort_field, ""),
                        reverse=reverse
                    )
                else:
                    transformed_data = sorted(data, reverse=reverse)
            
            else:
                # Identity transformation
                transformed_data = data.copy()
            
            result_data = {
                "transformed_data": transformed_data,
                "input_count": len(data),
                "output_count": len(transformed_data),
                "transformation": transformation,
                "parameters": transform_params
            }
            
            self._data_items_processed += len(data)
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Data transformation error: {e}"
            )
    
    def _filter_data(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Filter data operation."""
        # This is a specialized version of transform_data for filtering
        filter_params = parameters.copy()
        filter_params["transformation"] = "filter"
        return self._transform_data(filter_params, context)
    
    def _aggregate_data(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Aggregate data operation."""
        try:
            data = parameters.get("data", [])
            aggregation = parameters.get("aggregation", "count")
            group_by = parameters.get("group_by")
            field = parameters.get("field")
            
            if not data:
                return PluginExecutionResult(
                    success=False,
                    error="data parameter required"
                )
            
            if group_by and isinstance(data[0], dict):
                # Group by aggregation
                groups = {}
                for item in data:
                    group_key = item.get(group_by, "unknown")
                    if group_key not in groups:
                        groups[group_key] = []
                    groups[group_key].append(item)
                
                aggregated_data = {}
                for group_key, group_items in groups.items():
                    if aggregation == "count":
                        aggregated_data[group_key] = len(group_items)
                    elif aggregation == "sum" and field:
                        total = sum(float(item.get(field, 0)) for item in group_items)
                        aggregated_data[group_key] = total
                    elif aggregation == "average" and field:
                        total = sum(float(item.get(field, 0)) for item in group_items)
                        aggregated_data[group_key] = total / len(group_items)
                    elif aggregation == "min" and field:
                        values = [float(item.get(field, 0)) for item in group_items]
                        aggregated_data[group_key] = min(values)
                    elif aggregation == "max" and field:
                        values = [float(item.get(field, 0)) for item in group_items]
                        aggregated_data[group_key] = max(values)
                
            else:
                # Simple aggregation
                if aggregation == "count":
                    aggregated_data = {"total": len(data)}
                elif aggregation == "sum" and field:
                    total = sum(float(item.get(field, 0)) for item in data
                              if isinstance(item, dict))
                    aggregated_data = {"total": total}
                elif aggregation == "average" and field:
                    total = sum(float(item.get(field, 0)) for item in data
                              if isinstance(item, dict))
                    aggregated_data = {"average": total / len(data)}
                else:
                    aggregated_data = {"count": len(data)}
            
            result_data = {
                "aggregated_data": aggregated_data,
                "input_count": len(data),
                "aggregation": aggregation,
                "group_by": group_by,
                "field": field
            }
            
            self._data_items_processed += len(data)
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Data aggregation error: {e}"
            )
    
    def _validate_data(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Validate data operation."""
        try:
            data = parameters.get("data", [])
            validation_rules = parameters.get("validation_rules", {})
            
            if not data:
                return PluginExecutionResult(
                    success=False,
                    error="data parameter required"
                )
            
            validation_results = []
            valid_items = []
            invalid_items = []
            
            for i, item in enumerate(data):
                item_valid = True
                item_errors = []
                
                if isinstance(item, dict):
                    # Validate required fields
                    required_fields = validation_rules.get("required_fields", [])
                    for field in required_fields:
                        if field not in item or item[field] is None:
                            item_valid = False
                            item_errors.append(f"Missing required field: {field}")
                    
                    # Validate field types
                    field_types = validation_rules.get("field_types", {})
                    for field, expected_type in field_types.items():
                        if field in item:
                            if expected_type == "string" and not isinstance(item[field], str):
                                item_valid = False
                                item_errors.append(f"Field {field} must be string")
                            elif expected_type == "number" and not isinstance(item[field], (int, float)):
                                item_valid = False
                                item_errors.append(f"Field {field} must be number")
                    
                    # Validate field patterns
                    field_patterns = validation_rules.get("field_patterns", {})
                    for field, pattern in field_patterns.items():
                        if field in item and isinstance(item[field], str):
                            if not re.match(pattern, item[field]):
                                item_valid = False
                                item_errors.append(f"Field {field} does not match pattern")
                
                validation_result = {
                    "index": i,
                    "valid": item_valid,
                    "errors": item_errors
                }
                validation_results.append(validation_result)
                
                if item_valid:
                    valid_items.append(item)
                else:
                    invalid_items.append(item)
            
            result_data = {
                "validation_results": validation_results,
                "valid_items": valid_items,
                "invalid_items": invalid_items,
                "total_items": len(data),
                "valid_count": len(valid_items),
                "invalid_count": len(invalid_items),
                "validation_rules": validation_rules
            }
            
            self._data_items_processed += len(data)
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Data validation error: {e}"
            )
    
    def _process_text(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Process text operation."""
        try:
            text = parameters.get("text", "")
            operation_type = parameters.get("operation", "word_count")
            
            if not text:
                return PluginExecutionResult(
                    success=False,
                    error="text parameter required"
                )
            
            if operation_type == "word_count":
                words = text.split()
                lines = text.split('\n')
                characters = len(text)
                characters_no_spaces = len(text.replace(' ', ''))
                
                result_data = {
                    "word_count": len(words),
                    "line_count": len(lines),
                    "character_count": characters,
                    "character_count_no_spaces": characters_no_spaces,
                    "paragraph_count": len([p for p in text.split('\n\n') if p.strip()])
                }
                
            elif operation_type == "case_transform":
                transform_type = parameters.get("transform_type", "lower")
                
                if transform_type == "lower":
                    transformed_text = text.lower()
                elif transform_type == "upper":
                    transformed_text = text.upper()
                elif transform_type == "title":
                    transformed_text = text.title()
                elif transform_type == "capitalize":
                    transformed_text = text.capitalize()
                else:
                    transformed_text = text
                
                result_data = {
                    "original_text": text,
                    "transformed_text": transformed_text,
                    "transform_type": transform_type
                }
                
            elif operation_type == "clean_text":
                # Remove extra whitespace and normalize
                cleaned_text = re.sub(r'\s+', ' ', text.strip())
                
                # Remove special characters if requested
                remove_special = parameters.get("remove_special_chars", False)
                if remove_special:
                    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)
                
                result_data = {
                    "original_text": text,
                    "cleaned_text": cleaned_text,
                    "original_length": len(text),
                    "cleaned_length": len(cleaned_text)
                }
            
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unknown text operation: {operation_type}"
                )
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Text processing error: {e}"
            )
    
    def _extract_patterns(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Extract patterns from text operation."""
        try:
            text = parameters.get("text", "")
            pattern = parameters.get("pattern", "")
            pattern_type = parameters.get("pattern_type", "regex")
            
            if not text:
                return PluginExecutionResult(
                    success=False,
                    error="text parameter required"
                )
            
            matches = []
            
            if pattern_type == "regex":
                if not pattern:
                    return PluginExecutionResult(
                        success=False,
                        error="pattern parameter required for regex extraction"
                    )
                
                regex_matches = re.finditer(pattern, text)
                for match in regex_matches:
                    matches.append({
                        "match": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                        "groups": match.groups()
                    })
            
            elif pattern_type == "email":
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                regex_matches = re.finditer(email_pattern, text)
                for match in regex_matches:
                    matches.append({
                        "email": match.group(),
                        "start": match.start(),
                        "end": match.end()
                    })
            
            elif pattern_type == "url":
                url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                regex_matches = re.finditer(url_pattern, text)
                for match in regex_matches:
                    matches.append({
                        "url": match.group(),
                        "start": match.start(),
                        "end": match.end()
                    })
            
            elif pattern_type == "phone":
                phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
                regex_matches = re.finditer(phone_pattern, text)
                for match in regex_matches:
                    matches.append({
                        "phone": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                        "area_code": match.group(1),
                        "exchange": match.group(2),
                        "number": match.group(3)
                    })
            
            result_data = {
                "matches": matches,
                "match_count": len(matches),
                "pattern": pattern,
                "pattern_type": pattern_type,
                "text_length": len(text)
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Pattern extraction error: {e}"
            )
    
    def _format_text(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Format text operation."""
        try:
            text = parameters.get("text", "")
            format_type = parameters.get("format_type", "paragraph")
            format_params = parameters.get("format_parameters", {})
            
            if not text:
                return PluginExecutionResult(
                    success=False,
                    error="text parameter required"
                )
            
            if format_type == "paragraph":
                line_length = format_params.get("line_length", 80)
                words = text.split()
                lines = []
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > line_length and current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)
                    else:
                        current_line.append(word)
                        current_length += len(word) + (1 if current_line else 0)
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                formatted_text = '\n'.join(lines)
            
            elif format_type == "list":
                items = text.split('\n')
                list_type = format_params.get("list_type", "bullet")
                
                if list_type == "bullet":
                    formatted_text = '\n'.join([f"• {item.strip()}" for item in items if item.strip()])
                elif list_type == "numbered":
                    formatted_text = '\n'.join([f"{i+1}. {item.strip()}" for i, item in enumerate(items) if item.strip()])
                else:
                    formatted_text = text
            
            elif format_type == "code":
                language = format_params.get("language", "")
                if language:
                    formatted_text = f"```{language}\n{text}\n```"
                else:
                    formatted_text = f"```\n{text}\n```"
            
            else:
                formatted_text = text
            
            result_data = {
                "original_text": text,
                "formatted_text": formatted_text,
                "format_type": format_type,
                "format_parameters": format_params
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Text formatting error: {e}"
            )
    
    def _hash_data(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Hash data operation."""
        try:
            data = parameters.get("data", "")
            hash_algorithm = parameters.get("algorithm", "sha256")
            encoding = parameters.get("encoding", "utf-8")
            
            if not data:
                return PluginExecutionResult(
                    success=False,
                    error="data parameter required"
                )
            
            # Convert data to bytes if it's a string
            if isinstance(data, str):
                data_bytes = data.encode(encoding)
            elif isinstance(data, dict) or isinstance(data, list):
                data_bytes = json.dumps(data, sort_keys=True).encode(encoding)
            else:
                data_bytes = str(data).encode(encoding)
            
            # Generate hash
            if hash_algorithm == "md5":
                hash_obj = hashlib.md5(data_bytes)
            elif hash_algorithm == "sha1":
                hash_obj = hashlib.sha1(data_bytes)
            elif hash_algorithm == "sha256":
                hash_obj = hashlib.sha256(data_bytes)
            elif hash_algorithm == "sha512":
                hash_obj = hashlib.sha512(data_bytes)
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unsupported hash algorithm: {hash_algorithm}"
                )
            
            hash_digest = hash_obj.hexdigest()
            
            result_data = {
                "hash": hash_digest,
                "algorithm": hash_algorithm,
                "input_size": len(data_bytes),
                "encoding": encoding
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Hashing error: {e}"
            )
    
    def _encode_data(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Encode data operation."""
        try:
            data = parameters.get("data", "")
            encoding_type = parameters.get("encoding_type", "base64")
            input_encoding = parameters.get("input_encoding", "utf-8")
            
            if not data:
                return PluginExecutionResult(
                    success=False,
                    error="data parameter required"
                )
            
            # Convert data to bytes if it's a string
            if isinstance(data, str):
                data_bytes = data.encode(input_encoding)
            else:
                data_bytes = str(data).encode(input_encoding)
            
            if encoding_type == "base64":
                encoded_data = base64.b64encode(data_bytes).decode('ascii')
            elif encoding_type == "url":
                encoded_data = urllib.parse.quote(data.encode(input_encoding))
            elif encoding_type == "hex":
                encoded_data = data_bytes.hex()
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unsupported encoding type: {encoding_type}"
                )
            
            result_data = {
                "encoded_data": encoded_data,
                "encoding_type": encoding_type,
                "original_size": len(data_bytes),
                "encoded_size": len(encoded_data)
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Encoding error: {e}"
            )
    
    def _decode_data(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Decode data operation."""
        try:
            encoded_data = parameters.get("encoded_data", "")
            encoding_type = parameters.get("encoding_type", "base64")
            output_encoding = parameters.get("output_encoding", "utf-8")
            
            if not encoded_data:
                return PluginExecutionResult(
                    success=False,
                    error="encoded_data parameter required"
                )
            
            if encoding_type == "base64":
                decoded_bytes = base64.b64decode(encoded_data)
                decoded_data = decoded_bytes.decode(output_encoding)
            elif encoding_type == "url":
                decoded_data = urllib.parse.unquote(encoded_data)
            elif encoding_type == "hex":
                decoded_bytes = bytes.fromhex(encoded_data)
                decoded_data = decoded_bytes.decode(output_encoding)
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unsupported encoding type: {encoding_type}"
                )
            
            result_data = {
                "decoded_data": decoded_data,
                "encoding_type": encoding_type,
                "encoded_size": len(encoded_data),
                "decoded_size": len(decoded_data)
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Decoding error: {e}"
            )
    
    def _generate_id(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Generate ID operation."""
        try:
            id_type = parameters.get("id_type", "uuid")
            prefix = parameters.get("prefix", "")
            suffix = parameters.get("suffix", "")
            
            if id_type == "uuid":
                import uuid
                generated_id = str(uuid.uuid4())
            elif id_type == "timestamp":
                generated_id = str(int(time.time() * 1000))
            elif id_type == "random":
                import random
                import string
                length = parameters.get("length", 12)
                generated_id = ''.join(random.choices(
                    string.ascii_letters + string.digits,
                    k=length
                ))
            else:
                return PluginExecutionResult(
                    success=False,
                    error=f"Unsupported ID type: {id_type}"
                )
            
            # Add prefix and suffix
            full_id = f"{prefix}{generated_id}{suffix}"
            
            result_data = {
                "id": full_id,
                "id_type": id_type,
                "prefix": prefix,
                "suffix": suffix,
                "raw_id": generated_id
            }
            
            return PluginExecutionResult(success=True, result=result_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"ID generation error: {e}"
            )
    
    def _get_status(
        self,
        parameters: Dict[str, Any],
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        """Get plugin status operation."""
        try:
            status_data = {
                "plugin_status": {
                    "operations_performed": self._operations_performed,
                    "total_processing_time": self._total_processing_time,
                    "files_processed": self._files_processed,
                    "data_items_processed": self._data_items_processed,
                    "supported_operations": list(self._supported_operations.keys()),
                    "cached_results": len(self._cached_results)
                },
                "recent_operations": [
                    {
                        "operation": entry["operation"],
                        "success": entry["success"],
                        "execution_time": entry["execution_time"]
                    }
                    for entry in self._operation_history[-10:]  # Last 10 operations
                ]
            }
            
            return PluginExecutionResult(success=True, result=status_data)
            
        except Exception as e:
            return PluginExecutionResult(
                success=False,
                error=f"Status request failed: {e}"
            )
    
    def _get_data_size_info(self, data: Any) -> Dict[str, Any]:
        """Get size information for data structure."""
        try:
            if isinstance(data, dict):
                return {
                    "type": "dict",
                    "key_count": len(data),
                    "keys": list(data.keys())[:10]  # First 10 keys
                }
            elif isinstance(data, list):
                return {
                    "type": "list",
                    "item_count": len(data),
                    "item_types": list(set(type(item).__name__ for item in data[:100]))
                }
            else:
                return {
                    "type": type(data).__name__,
                    "string_length": len(str(data)) if hasattr(data, '__len__') else None
                }
        except Exception:
            return {"type": "unknown"}
    
    def _update_operation_history(
        self,
        operation: str,
        parameters: Dict[str, Any],
        result: PluginExecutionResult
    ):
        """Update operation history."""
        history_entry = {
            "operation": operation,
            "success": result.success,
            "execution_time": getattr(result, 'execution_time', 0.0),
            "timestamp": time.time(),
            "parameter_count": len(parameters)
        }
        
        self._operation_history.append(history_entry)
        
        # Keep only last 100 operations
        if len(self._operation_history) > 100:
            self._operation_history = self._operation_history[-100:]


# Plugin registration and example usage
if __name__ == "__main__":
    # Create plugin instance
    plugin = ExampleToolPlugin()
    
    # Initialize plugin
    init_context = {"logger": None}
    plugin.initialize(init_context)
    
    print("✅ Example Tool Plugin Implemented!")
    print(f"\nPlugin Metadata:")
    metadata = plugin.get_metadata()
    print(f"   Name: {metadata.name}")
    print(f"   Version: {metadata.version}")
    print(f"   Type: {metadata.plugin_type}")
    print(f"   Description: {metadata.description}")
    
    print(f"\nCapabilities: {[cap.value for cap in plugin.get_capabilities()]}")
    
    # Example data processing
    example_data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "Los Angeles"},
        {"name": "Bob", "age": 35, "city": "Chicago"},
        {"name": "Alice", "age": 28, "city": "New York"}
    ]
    
    # Test data transformation
    transform_context = PluginExecutionContext(
        correlation_id="test_001",
        operation="transform_data",
        parameters={
            "data": example_data,
            "transformation": "filter",
            "transform_parameters": {
                "field": "city",
                "value": "New York",
                "operator": "equals"
            }
        }
    )
    
    print(f"\nTesting Data Transformation...")
    transform_result = plugin.execute(transform_context)
    if transform_result.success:
        filtered_data = transform_result.result["transformed_data"]
        print(f"   Filtered {transform_result.result['input_count']} items to {transform_result.result['output_count']} items")
        print(f"   Results: {filtered_data}")
    
    # Test text processing
    text_context = PluginExecutionContext(
        correlation_id="test_002",
        operation="process_text",
        parameters={
            "text": "Hello World! This is a test of the Framework0 tool plugin.",
            "operation": "word_count"
        }
    )
    
    print(f"\nTesting Text Processing...")
    text_result = plugin.execute(text_context)
    if text_result.success:
        stats = text_result.result
        print(f"   Words: {stats['word_count']}")
        print(f"   Characters: {stats['character_count']}")
        print(f"   Lines: {stats['line_count']}")
    
    # Test pattern extraction
    pattern_context = PluginExecutionContext(
        correlation_id="test_003",
        operation="extract_patterns",
        parameters={
            "text": "Contact us at support@framework0.com or admin@example.org",
            "pattern_type": "email"
        }
    )
    
    print(f"\nTesting Pattern Extraction...")
    pattern_result = plugin.execute(pattern_context)
    if pattern_result.success:
        matches = pattern_result.result["matches"]
        print(f"   Found {len(matches)} email addresses:")
        for match in matches:
            print(f"     - {match['email']}")
    
    # Test hashing
    hash_context = PluginExecutionContext(
        correlation_id="test_004",
        operation="hash_data",
        parameters={
            "data": "Framework0 is awesome!",
            "algorithm": "sha256"
        }
    )
    
    print(f"\nTesting Data Hashing...")
    hash_result = plugin.execute(hash_context)
    if hash_result.success:
        hash_info = hash_result.result
        print(f"   SHA256 Hash: {hash_info['hash'][:16]}...")
        print(f"   Input Size: {hash_info['input_size']} bytes")
    
    print("\nKey Features Demonstrated:")
    print("   ✓ File operations (read, write, CSV, JSON)")
    print("   ✓ Data processing (transform, filter, aggregate, validate)")
    print("   ✓ Text processing (count, format, clean)")
    print("   ✓ Pattern extraction (regex, email, URL, phone)")
    print("   ✓ Utility functions (hash, encode, decode, generate ID)")
    print("   ✓ Comprehensive error handling")
    print("   ✓ Performance metrics tracking")
    print("   ✓ Operation history maintenance")
    
    # Cleanup
    plugin.cleanup()