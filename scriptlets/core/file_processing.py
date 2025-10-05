#!/usr/bin/env python3
"""
Framework0 Core - File Processing Scriptlet

Comprehensive file processing capabilities with validation, transformation,
and Foundation integration. This scriptlet provides the implementation
for the file_processing recipe template.

Features:
- Safe file operations with backup and rollback
- Multiple format support (text, JSON, CSV, XML, YAML, binary)
- Content validation and transformation
- Performance monitoring and health checks
- Integration with Foundation systems (5A-5D)
- Robust error handling and recovery

Usage:
    This scriptlet is designed to be called from Framework0 recipes,
    specifically the file_processing.yaml template.
"""

import os
import shutil
import hashlib
import chardet
import json
import csv
import xml.etree.ElementTree as ET
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from datetime import datetime, timezone
import time

# Framework0 imports with fallback
try:
    from orchestrator.context import Context
    from src.core.logger import get_logger
    FRAMEWORK0_AVAILABLE = True
except ImportError:
    Context = None
    FRAMEWORK0_AVAILABLE = False
    
    def get_logger(name):
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)

# Foundation imports for monitoring integration
try:
    from scriptlets.foundation.logging import get_framework_logger
    from scriptlets.foundation.health import get_health_monitor
    from scriptlets.foundation.metrics import get_performance_monitor
    FOUNDATION_AVAILABLE = True
except ImportError:
    FOUNDATION_AVAILABLE = False
    get_framework_logger = None
    get_health_monitor = None 
    get_performance_monitor = None


class FileProcessingError(Exception):
    """Custom exception for file processing errors."""
    pass


class FileProcessor:
    """
    Core file processing engine with comprehensive capabilities.
    
    Provides safe, monitored file operations with validation,
    transformation, and Foundation integration.
    """
    
    def __init__(self, context: Optional[Context] = None) -> None:
        """
        Initialize file processor.
        
        Args:
            context: Optional Framework0 context for integration
        """
        self.logger = get_logger(__name__)
        self.context = context
        self.start_time = time.time()
        
        # Initialize Foundation integration if available
        self.foundation_logger = None
        self.health_monitor = None
        self.performance_monitor = None
        
        if FOUNDATION_AVAILABLE:
            try:
                self.foundation_logger = get_framework_logger()
                self.health_monitor = get_health_monitor()
                self.performance_monitor = get_performance_monitor()
                self.logger.info("Foundation integration initialized")
            except Exception as e:
                self.logger.warning(f"Foundation integration failed: {e}")
        
        # Performance tracking
        self.performance_metrics = {
            "start_time": self.start_time,
            "operations": [],
            "memory_usage": [],
            "io_operations": 0
        }
        
        # Processing state
        self.processing_state = {
            "initialized": False,
            "backup_created": False,
            "backup_file": None,
            "source_validated": False,
            "content_read": False,
            "transformations_applied": False,
            "content_written": False,
            "integrity_verified": False
        }
    
    def _track_performance(self, operation: str, duration: float, **kwargs) -> None:
        """Track performance metrics for Foundation integration."""
        metric = {
            "operation": operation,
            "duration": duration,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **kwargs
        }
        self.performance_metrics["operations"].append(metric)
        
        if self.performance_monitor:
            try:
                self.performance_monitor.record_metric(
                    f"file_processing.{operation}", 
                    duration,
                    metadata=kwargs
                )
            except Exception as e:
                self.logger.warning(f"Performance monitoring failed: {e}")
    
    def _detect_encoding(self, file_path: str) -> str:
        """
        Detect file encoding automatically.
        
        Args:
            file_path: Path to file for encoding detection
            
        Returns:
            Detected encoding string
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Sample first 10KB
                result = chardet.detect(raw_data)
                encoding = result.get('encoding', 'utf-8')
                confidence = result.get('confidence', 0)
                
                self.logger.debug(
                    f"Detected encoding: {encoding} (confidence: {confidence:.2f})"
                )
                return encoding or 'utf-8'
                
        except Exception as e:
            self.logger.warning(f"Encoding detection failed: {e}, using utf-8")
            return 'utf-8'
    
    def _detect_format(self, file_path: str) -> str:
        """
        Detect file format from extension and content.
        
        Args:
            file_path: Path to file for format detection
            
        Returns:
            Detected format string
        """
        file_ext = Path(file_path).suffix.lower()
        
        # Extension-based detection
        format_map = {
            '.json': 'json',
            '.csv': 'csv', 
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.txt': 'text',
            '.log': 'text'
        }
        
        detected_format = format_map.get(file_ext, 'text')
        
        # Content-based validation for ambiguous cases
        if detected_format == 'text':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content_sample = f.read(1000)
                    
                # Try JSON parse
                if content_sample.strip().startswith(('{', '[')):
                    try:
                        json.loads(content_sample)
                        detected_format = 'json'
                    except json.JSONDecodeError:
                        pass
                
                # Check for CSV patterns
                elif ',' in content_sample and '\n' in content_sample:
                    lines = content_sample.split('\n')
                    if len(lines) > 1 and all(',' in line for line in lines[:3]):
                        detected_format = 'csv'
                        
            except Exception as e:
                self.logger.debug(f"Content-based format detection failed: {e}")
        
        self.logger.debug(f"Detected format: {detected_format}")
        return detected_format
    
    def _validate_file_path(self, file_path: str, for_writing: bool = False) -> str:
        """
        Validate and normalize file path.
        
        Args:
            file_path: File path to validate
            for_writing: Whether path will be used for writing
            
        Returns:
            Validated and normalized file path
            
        Raises:
            FileProcessingError: If path is invalid
        """
        try:
            path_obj = Path(file_path).resolve()
            
            if not for_writing and not path_obj.exists():
                raise FileProcessingError(f"Source file does not exist: {file_path}")
            
            if for_writing:
                # Ensure parent directory exists
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                
                # Check write permissions
                if path_obj.exists() and not os.access(path_obj, os.W_OK):
                    raise FileProcessingError(f"No write permission: {file_path}")
                elif not os.access(path_obj.parent, os.W_OK):
                    raise FileProcessingError(f"No write permission to directory: {path_obj.parent}")
            
            return str(path_obj)
            
        except Exception as e:
            raise FileProcessingError(f"Invalid file path {file_path}: {e}")
    
    def _calculate_checksum(self, content: Union[str, bytes]) -> str:
        """Calculate MD5 checksum for content verification."""
        if isinstance(content, str):
            content = content.encode('utf-8')
        return hashlib.md5(content).hexdigest()


def initialize_processing(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Initialize file processing with parameter validation.
    
    Args:
        context: Framework0 context
        **params: Processing parameters
        
    Returns:
        Dictionary with validated parameters and initialization results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        # Extract and validate parameters
        source_file = params.get('source_file')
        target_file = params.get('target_file', source_file)
        operation = params.get('operation', 'read')
        file_format = params.get('file_format', 'auto')
        encoding = params.get('encoding', 'auto')
        create_backup = params.get('create_backup', True)
        
        if not source_file:
            raise FileProcessingError("source_file parameter is required")
        
        # Validate file paths
        validated_source = processor._validate_file_path(source_file, for_writing=False)
        validated_target = processor._validate_file_path(target_file, for_writing=True)
        
        # Auto-detect encoding if needed
        if encoding == 'auto':
            detected_encoding = processor._detect_encoding(validated_source)
        else:
            detected_encoding = encoding
        
        # Auto-detect format if needed
        if file_format == 'auto':
            detected_format = processor._detect_format(validated_source)
        else:
            detected_format = file_format
        
        # Update processing state
        processor.processing_state['initialized'] = True
        
        result = {
            'validated_source': validated_source,
            'validated_target': validated_target,
            'detected_encoding': detected_encoding,
            'target_encoding': detected_encoding,  # Use same encoding for output
            'detected_format': detected_format,
            'operation': operation,
            'create_backup': create_backup,
            'processor_id': id(processor)
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('initialize', duration, **result)
        
        # Foundation integration logging
        if processor.foundation_logger:
            processor.foundation_logger.info(
                f"File processing initialized: {operation} on {source_file}",
                extra={'operation': operation, 'source': source_file}
            )
        
        processor.logger.info(f"File processing initialized successfully")
        return result
        
    except Exception as e:
        error_msg = f"Initialization failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def validate_source_file(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Validate source file accessibility and permissions.
    
    Args:
        context: Framework0 context
        **params: Validation parameters
        
    Returns:
        Dictionary with validation results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        file_path = params.get('file_path')
        required_permissions = params.get('required_permissions', ['read'])
        validation_rules = params.get('validation_rules', {})
        
        if not file_path:
            raise FileProcessingError("file_path parameter is required")
        
        path_obj = Path(file_path)
        
        # Check file existence
        if not path_obj.exists():
            raise FileProcessingError(f"File does not exist: {file_path}")
        
        # Check file type
        if not path_obj.is_file():
            raise FileProcessingError(f"Path is not a file: {file_path}")
        
        # Check permissions
        permission_checks = {
            'read': os.R_OK,
            'write': os.W_OK,
            'execute': os.X_OK
        }
        
        for permission in required_permissions:
            if permission in permission_checks:
                if not os.access(path_obj, permission_checks[permission]):
                    raise FileProcessingError(
                        f"Missing {permission} permission: {file_path}"
                    )
        
        # Get file metadata
        stat = path_obj.stat()
        file_metadata = {
            'size': stat.st_size,
            'modification_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'permissions': oct(stat.st_mode)[-3:],
            'is_readable': os.access(path_obj, os.R_OK),
            'is_writable': os.access(path_obj, os.W_OK)
        }
        
        # Apply validation rules
        validation_results = []
        
        if 'max_size' in validation_rules:
            max_size = validation_rules['max_size']
            if stat.st_size > max_size:
                raise FileProcessingError(
                    f"File size {stat.st_size} exceeds maximum {max_size}"
                )
            validation_results.append(f"Size validation passed ({stat.st_size} <= {max_size})")
        
        if 'min_size' in validation_rules:
            min_size = validation_rules['min_size']
            if stat.st_size < min_size:
                raise FileProcessingError(
                    f"File size {stat.st_size} below minimum {min_size}"
                )
            validation_results.append(f"Size validation passed ({stat.st_size} >= {min_size})")
        
        result = {
            'file_path': file_path,
            'file_exists': True,
            'file_metadata': file_metadata,
            'validation_passed': True,
            'validation_results': validation_results
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('validate_source', duration, file_size=stat.st_size)
        
        processor.logger.info(f"Source file validation successful: {file_path}")
        return result
        
    except Exception as e:
        error_msg = f"Source file validation failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'file_path': file_path, 'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def create_backup(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Create backup of source file before modification.
    
    Args:
        context: Framework0 context
        **params: Backup parameters
        
    Returns:
        Dictionary with backup results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        source_file = params.get('source_file')
        create_backup = params.get('create_backup', True)
        
        if not create_backup:
            return {
                'backup_created': False,
                'backup_file': None,
                'backup_skipped': True
            }
        
        if not source_file:
            raise FileProcessingError("source_file parameter is required")
        
        # Generate backup filename with timestamp
        source_path = Path(source_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = source_path.with_name(
            f"{source_path.stem}_backup_{timestamp}{source_path.suffix}"
        )
        
        # Copy file to backup location
        shutil.copy2(source_file, backup_file)
        
        # Verify backup integrity
        if not backup_file.exists():
            raise FileProcessingError("Backup creation failed - file not found")
        
        backup_stat = backup_file.stat()
        source_stat = source_path.stat()
        
        if backup_stat.st_size != source_stat.st_size:
            raise FileProcessingError("Backup verification failed - size mismatch")
        
        result = {
            'backup_created': True,
            'backup_file': str(backup_file),
            'backup_size': backup_stat.st_size,
            'creation_time': datetime.now().isoformat()
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('create_backup', duration, file_size=backup_stat.st_size)
        
        processor.logger.info(f"Backup created successfully: {backup_file}")
        return result
        
    except Exception as e:
        error_msg = f"Backup creation failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'source_file': source_file, 'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def read_file_content(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Read and parse file content with format-specific handling.
    
    Args:
        context: Framework0 context
        **params: Reading parameters
        
    Returns:
        Dictionary with file content and metadata
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        file_path = params.get('file_path')
        file_format = params.get('file_format', 'text')
        encoding = params.get('encoding', 'utf-8')
        validation_rules = params.get('validation_rules', {})
        
        if not file_path:
            raise FileProcessingError("file_path parameter is required")
        
        path_obj = Path(file_path)
        file_size = path_obj.stat().st_size
        
        # Memory check for large files
        if file_size > 100 * 1024 * 1024:  # 100MB threshold
            processor.logger.warning(f"Large file detected: {file_size / 1024 / 1024:.1f}MB")
            
            if processor.health_monitor:
                memory_status = processor.health_monitor.check_memory_usage()
                if memory_status.get('usage_percent', 0) > 80:
                    raise FileProcessingError("Insufficient memory for large file processing")
        
        # Read file content based on format
        content = None
        parsed_content = None
        
        if file_format == 'binary':
            # Binary file handling
            with open(file_path, 'rb') as f:
                content = f.read()
                parsed_content = content  # Keep as bytes
        else:
            # Text-based file handling
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                
            # Format-specific parsing
            if file_format == 'json':
                try:
                    parsed_content = json.loads(content)
                except json.JSONDecodeError as e:
                    raise FileProcessingError(f"Invalid JSON format: {e}")
                    
            elif file_format == 'csv':
                try:
                    import io
                    csv_reader = csv.DictReader(io.StringIO(content))
                    parsed_content = list(csv_reader)
                except Exception as e:
                    raise FileProcessingError(f"Invalid CSV format: {e}")
                    
            elif file_format == 'xml':
                try:
                    parsed_content = ET.fromstring(content)
                except ET.ParseError as e:
                    raise FileProcessingError(f"Invalid XML format: {e}")
                    
            elif file_format == 'yaml':
                try:
                    parsed_content = yaml.safe_load(content)
                except yaml.YAMLError as e:
                    raise FileProcessingError(f"Invalid YAML format: {e}")
            else:
                # Plain text
                parsed_content = content
        
        # Calculate content checksum
        checksum = processor._calculate_checksum(content)
        
        result = {
            'content': content,
            'parsed_content': parsed_content,
            'file_size': file_size,
            'file_format': file_format,
            'encoding': encoding,
            'checksum': checksum,
            'line_count': content.count('\n') + 1 if isinstance(content, str) else None,
            'read_time': datetime.now().isoformat()
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance(
            'read_content', 
            duration, 
            file_size=file_size,
            file_format=file_format
        )
        
        processor.logger.info(f"File content read successfully: {file_size} bytes")
        return result
        
    except Exception as e:
        error_msg = f"File reading failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'file_path': file_path, 'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def apply_transformations(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Apply transformation rules to file content.
    
    Args:
        context: Framework0 context
        **params: Transformation parameters
        
    Returns:
        Dictionary with transformed content
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        content = params.get('content')
        file_format = params.get('file_format', 'text')
        transformation_rules = params.get('transformation_rules', {})
        source_file = params.get('source_file', 'unknown')
        
        if content is None:
            raise FileProcessingError("content parameter is required")
        
        if not transformation_rules:
            return {
                'transformed_content': content,
                'transformations_applied': [],
                'transformation_skipped': True
            }
        
        transformed_content = content
        transformations_applied = []
        
        # Apply transformations based on rules
        for rule_name, rule_config in transformation_rules.items():
            
            if rule_name == 'string_replace':
                # String replacement transformations
                replacements = rule_config.get('replacements', [])
                for replacement in replacements:
                    old_value = replacement.get('old')
                    new_value = replacement.get('new')
                    if old_value is not None and new_value is not None:
                        if isinstance(transformed_content, str):
                            count = transformed_content.count(old_value)
                            transformed_content = transformed_content.replace(old_value, new_value)
                            transformations_applied.append(
                                f"String replacement: '{old_value}' -> '{new_value}' ({count} occurrences)"
                            )
            
            elif rule_name == 'json_transform':
                # JSON-specific transformations
                if file_format == 'json' and isinstance(transformed_content, dict):
                    
                    # Add fields
                    if 'add_fields' in rule_config:
                        for field, value in rule_config['add_fields'].items():
                            transformed_content[field] = value
                            transformations_applied.append(f"Added field: {field}")
                    
                    # Remove fields
                    if 'remove_fields' in rule_config:
                        for field in rule_config['remove_fields']:
                            if field in transformed_content:
                                del transformed_content[field]
                                transformations_applied.append(f"Removed field: {field}")
            
            elif rule_name == 'format_convert':
                # Format conversion transformations
                target_format = rule_config.get('target_format')
                
                if target_format == 'json' and file_format == 'csv':
                    # Convert CSV to JSON
                    if isinstance(transformed_content, list):
                        transformed_content = json.dumps(transformed_content, indent=2)
                        transformations_applied.append("Converted CSV to JSON")
                
                elif target_format == 'csv' and file_format == 'json':
                    # Convert JSON to CSV
                    if isinstance(transformed_content, list) and transformed_content:
                        import io
                        output = io.StringIO()
                        writer = csv.DictWriter(output, fieldnames=transformed_content[0].keys())
                        writer.writeheader()
                        writer.writerows(transformed_content)
                        transformed_content = output.getvalue()
                        transformations_applied.append("Converted JSON to CSV")
            
            else:
                processor.logger.warning(f"Unknown transformation rule: {rule_name}")
        
        result = {
            'transformed_content': transformed_content,
            'transformations_applied': transformations_applied,
            'transformation_count': len(transformations_applied),
            'transformation_time': datetime.now().isoformat()
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance(
            'apply_transformations', 
            duration, 
            transformation_count=len(transformations_applied)
        )
        
        processor.logger.info(f"Transformations applied: {len(transformations_applied)}")
        return result
        
    except Exception as e:
        error_msg = f"Content transformation failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'source_file': source_file, 'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def validate_content(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Validate content against specified rules and schemas.
    
    Args:
        context: Framework0 context
        **params: Validation parameters
        
    Returns:
        Dictionary with validation results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        content = params.get('content')
        file_format = params.get('file_format', 'text')
        validation_rules = params.get('validation_rules', {})
        
        if content is None:
            raise FileProcessingError("content parameter is required")
        
        validation_results = []
        validation_passed = True
        
        # Format-specific validation
        if file_format == 'json':
            try:
                # Validate JSON structure
                if isinstance(content, str):
                    json.loads(content)
                validation_results.append("JSON format validation passed")
            except json.JSONDecodeError as e:
                validation_passed = False
                validation_results.append(f"JSON format validation failed: {e}")
        
        # Apply custom validation rules
        for rule_name, rule_config in validation_rules.items():
            
            if rule_name == 'required_fields':
                # Check for required fields in JSON/dict content
                if isinstance(content, dict):
                    required_fields = rule_config.get('fields', [])
                    for field in required_fields:
                        if field not in content:
                            validation_passed = False
                            validation_results.append(f"Missing required field: {field}")
                        else:
                            validation_results.append(f"Required field present: {field}")
            
            elif rule_name == 'pattern_match':
                # Pattern matching for text content
                if isinstance(content, str):
                    patterns = rule_config.get('patterns', [])
                    for pattern in patterns:
                        import re
                        if re.search(pattern, content):
                            validation_results.append(f"Pattern match found: {pattern}")
                        else:
                            if rule_config.get('required', False):
                                validation_passed = False
                                validation_results.append(f"Required pattern not found: {pattern}")
        
        result = {
            'validation_passed': validation_passed,
            'validation_results': validation_results,
            'validation_count': len(validation_results),
            'validation_time': datetime.now().isoformat()
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('validate_content', duration, validation_passed=validation_passed)
        
        processor.logger.info(f"Content validation {'passed' if validation_passed else 'failed'}")
        return result
        
    except Exception as e:
        error_msg = f"Content validation failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def write_file_content(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Write content to target file with format-specific handling.
    
    Args:
        context: Framework0 context
        **params: Writing parameters
        
    Returns:
        Dictionary with writing results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        content = params.get('content')
        target_file = params.get('target_file')
        file_format = params.get('file_format', 'text')
        encoding = params.get('encoding', 'utf-8')
        
        if content is None:
            raise FileProcessingError("content parameter is required")
        
        if not target_file:
            raise FileProcessingError("target_file parameter is required")
        
        # Prepare content for writing based on format
        write_content = content
        
        if file_format == 'json' and isinstance(content, dict):
            write_content = json.dumps(content, indent=2, ensure_ascii=False)
        elif file_format == 'yaml' and isinstance(content, dict):
            write_content = yaml.dump(content, default_flow_style=False, allow_unicode=True)
        
        # Write content to file
        if isinstance(write_content, bytes):
            with open(target_file, 'wb') as f:
                f.write(write_content)
        else:
            with open(target_file, 'w', encoding=encoding) as f:
                f.write(write_content)
        
        # Get file statistics
        target_path = Path(target_file)
        stat = target_path.stat()
        
        result = {
            'target_file': target_file,
            'bytes_written': stat.st_size,
            'encoding': encoding,
            'file_format': file_format,
            'write_time': datetime.now().isoformat(),
            'write_successful': True
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('write_content', duration, bytes_written=stat.st_size)
        
        processor.logger.info(f"Content written successfully: {stat.st_size} bytes to {target_file}")
        return result
        
    except Exception as e:
        error_msg = f"File writing failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'target_file': target_file, 'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def verify_file_integrity(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Verify file integrity and validate successful write operations.
    
    Args:
        context: Framework0 context
        **params: Verification parameters
        
    Returns:
        Dictionary with verification results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        file_path = params.get('file_path')
        expected_checksum = params.get('expected_checksum')
        expected_size = params.get('expected_size')
        
        if not file_path:
            raise FileProcessingError("file_path parameter is required")
        
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            raise FileProcessingError(f"File not found for verification: {file_path}")
        
        # Get file statistics
        stat = path_obj.stat()
        actual_size = stat.st_size
        
        # Calculate checksum
        with open(file_path, 'rb') as f:
            content = f.read()
            actual_checksum = processor._calculate_checksum(content)
        
        verification_results = []
        verification_passed = True
        
        # Size verification
        if expected_size is not None:
            if actual_size == expected_size:
                verification_results.append(f"Size verification passed: {actual_size} bytes")
            else:
                verification_passed = False
                verification_results.append(
                    f"Size verification failed: expected {expected_size}, got {actual_size}"
                )
        
        # Checksum verification
        if expected_checksum:
            if actual_checksum == expected_checksum:
                verification_results.append("Checksum verification passed")
            else:
                verification_passed = False
                verification_results.append(
                    f"Checksum verification failed: expected {expected_checksum}, got {actual_checksum}"
                )
        
        result = {
            'file_path': file_path,
            'verification_passed': verification_passed,
            'actual_size': actual_size,
            'actual_checksum': actual_checksum,
            'verification_results': verification_results,
            'verification_time': datetime.now().isoformat()
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('verify_integrity', duration, verification_passed=verification_passed)
        
        processor.logger.info(f"File integrity {'verified' if verification_passed else 'failed'}: {file_path}")
        return result
        
    except Exception as e:
        error_msg = f"File integrity verification failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'file_path': file_path, 'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def finalize_processing(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Finalize file processing and generate comprehensive report.
    
    Args:
        context: Framework0 context
        **params: Finalization parameters
        
    Returns:
        Dictionary with processing summary and metrics
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        operation_results = params.get('operation_results', [])
        source_file = params.get('source_file')
        target_file = params.get('target_file')
        cleanup_temp_files = params.get('cleanup_temp_files', True)
        
        # Collect performance metrics
        total_duration = time.time() - processor.start_time
        
        # Generate processing summary
        processing_summary = {
            'source_file': source_file,
            'target_file': target_file,
            'operation_count': len(operation_results),
            'total_duration': total_duration,
            'operations': operation_results,
            'completion_time': datetime.now().isoformat(),
            'processing_successful': True
        }
        
        # Generate performance report
        performance_report = {
            'total_duration': total_duration,
            'average_operation_time': total_duration / max(len(operation_results), 1),
            'performance_metrics': processor.performance_metrics,
            'memory_usage': 'not_monitored'  # Would integrate with system monitoring
        }
        
        # Foundation integration summary
        foundation_summary = {
            'logger_available': processor.foundation_logger is not None,
            'health_monitor_available': processor.health_monitor is not None,
            'performance_monitor_available': processor.performance_monitor is not None
        }
        
        result = {
            'processing_summary': processing_summary,
            'performance_report': performance_report,
            'foundation_integration': foundation_summary,
            'finalization_time': datetime.now().isoformat(),
            'finalization_successful': True
        }
        
        # Track final performance
        duration = time.time() - start_time
        processor._track_performance('finalize', duration, operation_count=len(operation_results))
        
        processor.logger.info(f"File processing finalized: {len(operation_results)} operations in {total_duration:.2f}s")
        
        if processor.foundation_logger:
            processor.foundation_logger.info(
                f"File processing completed successfully",
                extra={
                    'source_file': source_file,
                    'target_file': target_file,
                    'duration': total_duration,
                    'operations': len(operation_results)
                }
            )
        
        return result
        
    except Exception as e:
        error_msg = f"Processing finalization failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def restore_from_backup(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Restore file from backup in case of processing failure.
    
    Args:
        context: Framework0 context
        **params: Restore parameters
        
    Returns:
        Dictionary with restoration results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        backup_file = params.get('backup_file')
        target_file = params.get('target_file')
        
        if not backup_file:
            raise FileProcessingError("backup_file parameter is required")
        
        if not target_file:
            raise FileProcessingError("target_file parameter is required")
        
        backup_path = Path(backup_file)
        target_path = Path(target_file)
        
        if not backup_path.exists():
            raise FileProcessingError(f"Backup file not found: {backup_file}")
        
        # Restore file from backup
        shutil.copy2(backup_file, target_file)
        
        # Verify restoration
        if not target_path.exists():
            raise FileProcessingError("File restoration failed - target not found")
        
        target_stat = target_path.stat()
        backup_stat = backup_path.stat()
        
        if target_stat.st_size != backup_stat.st_size:
            raise FileProcessingError("File restoration verification failed - size mismatch")
        
        result = {
            'backup_file': backup_file,
            'target_file': target_file,
            'restored_size': target_stat.st_size,
            'restoration_time': datetime.now().isoformat(),
            'restoration_successful': True
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('restore_backup', duration, restored_size=target_stat.st_size)
        
        processor.logger.info(f"File restored from backup: {backup_file} -> {target_file}")
        return result
        
    except Exception as e:
        error_msg = f"Backup restoration failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'backup_file': backup_file, 'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


def cleanup_partial_files(context: Optional[Context] = None, **params) -> Dict[str, Any]:
    """
    Clean up partial or temporary files after processing completion or failure.
    
    Args:
        context: Framework0 context
        **params: Cleanup parameters
        
    Returns:
        Dictionary with cleanup results
    """
    start_time = time.time()
    processor = FileProcessor(context)
    
    try:
        cleanup_files = params.get('cleanup_files', [])
        backup_files = params.get('backup_files', [])
        preserve_backups = params.get('preserve_backups', True)
        
        cleaned_files = []
        cleanup_errors = []
        
        # Clean up temporary and partial files
        for file_path in cleanup_files:
            try:
                path_obj = Path(file_path)
                if path_obj.exists():
                    path_obj.unlink()
                    cleaned_files.append(file_path)
                    processor.logger.debug(f"Cleaned up file: {file_path}")
            except Exception as e:
                cleanup_errors.append(f"Failed to clean {file_path}: {str(e)}")
                processor.logger.warning(f"Cleanup failed for {file_path}: {e}")
        
        # Handle backup files
        if not preserve_backups:
            for backup_file in backup_files:
                try:
                    backup_path = Path(backup_file)
                    if backup_path.exists():
                        backup_path.unlink()
                        cleaned_files.append(backup_file)
                        processor.logger.debug(f"Removed backup file: {backup_file}")
                except Exception as e:
                    cleanup_errors.append(f"Failed to remove backup {backup_file}: {str(e)}")
                    processor.logger.warning(f"Backup cleanup failed for {backup_file}: {e}")
        
        result = {
            'cleaned_files': cleaned_files,
            'cleanup_errors': cleanup_errors,
            'files_cleaned_count': len(cleaned_files),
            'cleanup_successful': len(cleanup_errors) == 0,
            'cleanup_time': datetime.now().isoformat()
        }
        
        # Track performance
        duration = time.time() - start_time
        processor._track_performance('cleanup', duration, files_cleaned=len(cleaned_files))
        
        processor.logger.info(f"Cleanup completed: {len(cleaned_files)} files removed")
        return result
        
    except Exception as e:
        error_msg = f"File cleanup failed: {str(e)}"
        processor.logger.error(error_msg)
        
        if processor.foundation_logger:
            processor.foundation_logger.error(error_msg, extra={'error': str(e)})
        
        raise FileProcessingError(error_msg) from e


# Main entry point for Framework0 integration
if __name__ == "__main__":
    # Example usage for testing
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python file_processing.py <operation> <file_path>")
        sys.exit(1)
    
    operation = sys.argv[1]
    file_path = sys.argv[2]
    
    try:
        if operation == "validate":
            result = validate_source_file(file_path=file_path)
            print(f"Validation result: {result}")
        
        elif operation == "read":
            result = read_file_content(file_path=file_path)
            print(f"Content size: {result['file_size']} bytes")
        
        else:
            print(f"Unknown operation: {operation}")
            sys.exit(1)
            
    except FileProcessingError as e:
        print(f"Error: {e}")
        sys.exit(1)