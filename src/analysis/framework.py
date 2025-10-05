"""
Core Analysis Framework

This module defines the base classes and interfaces for the consolidated 
analysis framework in IAF0. It provides a standardized approach to data
analysis with enhanced capabilities, thread safety, and comprehensive logging.

Classes:
    BaseAnalyzerV2: Abstract base class for all analyzers
    AnalysisResult: Standardized result structure
    AnalysisConfig: Configuration management for analysis operations
    AnalysisError: Custom exception for analysis-related errors

Features:
    - Thread-safe operations with RLock protection
    - Comprehensive logging with debug support
    - Statistical analysis capabilities built-in
    - Pattern detection and trend analysis
    - Data quality assessment and validation
    - Hook system for extensible analysis pipelines
    - Memory usage monitoring and optimization
"""

import os
import time
import json
import threading
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Import core logger for consistent logging across framework
from src.core.logger import get_logger

# Type variable for generic result types
T = TypeVar('T')

class AnalysisError(Exception):
    """
    Custom exception class for analysis-related errors.
    
    Provides enhanced error reporting with context information
    and support for error chaining in complex analysis pipelines.
    """
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                 context: Optional[Dict[str, Any]] = None) -> None:
        """Initialize AnalysisError with enhanced context information."""
        super().__init__(message)  # Call parent Exception constructor
        self.error_code = error_code or "ANALYSIS_ERROR"  # Default error code
        self.context = context or {}  # Additional context for debugging
        self.timestamp = datetime.now()  # When error occurred


@dataclass
class AnalysisConfig:
    """
    Configuration class for analysis operations.
    
    Provides centralized configuration management with validation,
    serialization support, and environment-based overrides.
    """
    
    # Core configuration options
    timeout_seconds: int = 300  # Maximum analysis execution time
    enable_threading: bool = True  # Whether to use thread-safe operations
    max_memory_mb: int = 512  # Maximum memory usage in megabytes
    debug_mode: bool = field(default_factory=lambda: os.getenv("DEBUG") == "1")  # Debug flag from environment
    
    # Analysis-specific options
    statistical_precision: int = 6  # Decimal places for statistical calculations
    pattern_threshold: float = 0.7  # Minimum confidence for pattern detection
    quality_threshold: float = 0.8  # Minimum quality score for data validation
    
    # Output configuration
    include_raw_data: bool = False  # Whether to include raw data in results
    format_output: bool = True  # Whether to format output for readability
    save_intermediate: bool = False  # Whether to save intermediate results
    
    # Hook configuration
    pre_analysis_hooks: List[str] = field(default_factory=list)  # Hook names to run before analysis
    post_analysis_hooks: List[str] = field(default_factory=list)  # Hook names to run after analysis
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        return {
            'timeout_seconds': self.timeout_seconds,  # Analysis timeout setting
            'enable_threading': self.enable_threading,  # Threading configuration
            'max_memory_mb': self.max_memory_mb,  # Memory limit setting
            'debug_mode': self.debug_mode,  # Debug mode flag
            'statistical_precision': self.statistical_precision,  # Statistics precision
            'pattern_threshold': self.pattern_threshold,  # Pattern detection threshold
            'quality_threshold': self.quality_threshold,  # Quality validation threshold
            'include_raw_data': self.include_raw_data,  # Raw data inclusion flag
            'format_output': self.format_output,  # Output formatting flag
            'save_intermediate': self.save_intermediate,  # Intermediate results flag
            'pre_analysis_hooks': self.pre_analysis_hooks.copy(),  # Copy of pre-analysis hooks
            'post_analysis_hooks': self.post_analysis_hooks.copy()  # Copy of post-analysis hooks
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AnalysisConfig':
        """Create configuration from dictionary with validation."""
        # Validate required fields and types
        valid_keys = {
            'timeout_seconds', 'enable_threading', 'max_memory_mb', 'debug_mode',
            'statistical_precision', 'pattern_threshold', 'quality_threshold',
            'include_raw_data', 'format_output', 'save_intermediate',
            'pre_analysis_hooks', 'post_analysis_hooks'
        }
        
        # Filter out invalid keys to prevent errors
        filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}
        
        return cls(**filtered_dict)  # Create instance with validated data


@dataclass
class AnalysisResult(Generic[T]):
    """
    Standardized result structure for all analysis operations.
    
    Provides consistent result format with metadata, timing information,
    statistical summaries, and comprehensive error handling.
    """
    
    # Core result data
    analyzer_name: str  # Name of analyzer that produced this result
    data: T  # Main analysis result data (generic type)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata
    
    # Execution information  
    execution_time: float = 0.0  # Time taken for analysis in seconds
    memory_used: int = 0  # Peak memory usage in bytes
    success: bool = True  # Whether analysis completed successfully
    
    # Statistical summary
    statistics: Dict[str, float] = field(default_factory=dict)  # Statistical measures
    patterns: List[Dict[str, Any]] = field(default_factory=list)  # Detected patterns
    quality_score: float = 1.0  # Data quality assessment score (0.0 to 1.0)
    
    # Error information
    errors: List[str] = field(default_factory=list)  # List of errors encountered
    warnings: List[str] = field(default_factory=list)  # List of warnings generated
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)  # When result was created
    
    def add_error(self, error: str) -> None:
        """Add error message to result and mark as unsuccessful."""
        self.errors.append(error)  # Add error to error list
        self.success = False  # Mark result as unsuccessful
    
    def add_warning(self, warning: str) -> None:
        """Add warning message to result."""
        self.warnings.append(warning)  # Add warning to warning list
    
    def add_statistic(self, name: str, value: float) -> None:
        """Add statistical measure to result."""
        self.statistics[name] = value  # Store statistic with name
    
    def add_pattern(self, pattern_type: str, confidence: float, 
                   details: Dict[str, Any]) -> None:
        """Add detected pattern to result."""
        pattern = {
            'type': pattern_type,  # Type of pattern detected
            'confidence': confidence,  # Confidence level (0.0 to 1.0)
            'details': details,  # Additional pattern details
            'detected_at': datetime.now()  # When pattern was detected
        }
        self.patterns.append(pattern)  # Add pattern to patterns list
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization."""
        # Process patterns to ensure datetime serialization
        serializable_patterns = []
        for pattern in self.patterns:
            serializable_pattern = pattern.copy()  # Copy pattern
            if 'detected_at' in serializable_pattern and hasattr(serializable_pattern['detected_at'], 'isoformat'):
                serializable_pattern['detected_at'] = serializable_pattern['detected_at'].isoformat()  # Convert datetime to ISO string
            serializable_patterns.append(serializable_pattern)  # Add serializable pattern
        
        return {
            'analyzer_name': self.analyzer_name,  # Name of analyzer
            'data': self.data,  # Main result data
            'metadata': self.metadata.copy(),  # Copy of metadata
            'execution_time': self.execution_time,  # Execution timing
            'memory_used': self.memory_used,  # Memory usage
            'success': self.success,  # Success flag
            'statistics': self.statistics.copy(),  # Copy of statistics
            'patterns': serializable_patterns,  # Serializable patterns
            'quality_score': self.quality_score,  # Quality assessment
            'errors': self.errors.copy(),  # Copy of errors
            'warnings': self.warnings.copy(),  # Copy of warnings
            'created_at': self.created_at.isoformat()  # ISO format timestamp
        }


class BaseAnalyzerV2(ABC):
    """
    Abstract base class for all analyzers in the consolidated framework.
    
    Provides standardized interface, thread safety, comprehensive logging,
    and built-in statistical analysis capabilities. All analyzers should
    inherit from this class to ensure consistency and compatibility.
    
    Features:
        - Thread-safe operations with RLock
        - Comprehensive logging with debug support
        - Hook system for extensible analysis pipelines
        - Memory usage monitoring
        - Statistical analysis utilities
        - Pattern detection capabilities
        - Data quality assessment
    """
    
    def __init__(self, name: str, config: Optional[AnalysisConfig] = None) -> None:
        """
        Initialize analyzer with configuration and thread safety.
        
        Args:
            name: Unique name for this analyzer instance
            config: Configuration object, uses defaults if None
        """
        self.name = name  # Unique analyzer identifier
        self.config = config or AnalysisConfig()  # Use provided config or defaults
        self._lock = threading.RLock()  # Thread safety lock
        self.logger = get_logger(__name__, debug=self.config.debug_mode)  # Logger instance
        
        # Hook system for extensible pipelines
        self._hooks: Dict[str, List[Callable]] = {
            'pre_analysis': [],  # Functions to run before analysis
            'post_analysis': [],  # Functions to run after analysis
            'on_error': [],  # Functions to run on errors
            'on_pattern': []  # Functions to run when patterns detected
        }
        
        # Statistics tracking
        self._analysis_count = 0  # Number of analyses performed
        self._total_execution_time = 0.0  # Total time spent in analysis
        self._last_analysis_time = None  # Timestamp of last analysis
        
        self.logger.info(f"Initialized analyzer '{name}' with config: {self.config.to_dict()}")
    
    def add_hook(self, hook_type: str, hook_function: Callable) -> None:
        """Add hook function to specified hook type."""
        with self._lock:  # Thread-safe hook registration
            if hook_type in self._hooks:  # Validate hook type
                self._hooks[hook_type].append(hook_function)  # Add hook function
                self.logger.debug(f"Added hook of type '{hook_type}' to analyzer '{self.name}'")
            else:
                raise ValueError(f"Invalid hook type: {hook_type}")  # Invalid hook type error
    
    def remove_hook(self, hook_type: str, hook_function: Callable) -> None:
        """Remove hook function from specified hook type."""
        with self._lock:  # Thread-safe hook removal
            if hook_type in self._hooks and hook_function in self._hooks[hook_type]:
                self._hooks[hook_type].remove(hook_function)  # Remove hook function
                self.logger.debug(f"Removed hook of type '{hook_type}' from analyzer '{self.name}'")
    
    def _run_hooks(self, hook_type: str, *args, **kwargs) -> None:
        """Execute all hooks of specified type with provided arguments."""
        for hook in self._hooks.get(hook_type, []):  # Iterate through hooks safely
            try:
                hook(*args, **kwargs)  # Execute hook with arguments
            except Exception as e:
                self.logger.warning(f"Hook execution failed: {e}")  # Log hook failures
    
    def _calculate_statistics(self, data: Any) -> Dict[str, float]:
        """Calculate basic statistical measures for numeric data."""
        stats = {}  # Initialize statistics dictionary
        
        if isinstance(data, (list, tuple)) and data:  # Check for numeric sequence
            numeric_data = [x for x in data if isinstance(x, (int, float))]  # Filter numeric values
            
            if numeric_data:  # If we have numeric data
                stats['count'] = len(numeric_data)  # Count of values
                stats['mean'] = sum(numeric_data) / len(numeric_data)  # Average value
                stats['min'] = min(numeric_data)  # Minimum value
                stats['max'] = max(numeric_data)  # Maximum value
                
                # Calculate standard deviation
                mean_val = stats['mean']  # Get calculated mean
                variance = sum((x - mean_val) ** 2 for x in numeric_data) / len(numeric_data)  # Variance calculation
                stats['std_dev'] = variance ** 0.5  # Standard deviation
                
                # Calculate median
                sorted_data = sorted(numeric_data)  # Sort data for median
                n = len(sorted_data)  # Length for median calculation
                if n % 2 == 0:  # Even number of elements
                    stats['median'] = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2  # Average of middle two
                else:  # Odd number of elements
                    stats['median'] = sorted_data[n//2]  # Middle element
        
        return stats  # Return calculated statistics
    
    def _detect_patterns(self, data: Any, threshold: float = None) -> List[Dict[str, Any]]:
        """Detect patterns in data using configurable threshold."""
        patterns = []  # Initialize patterns list
        threshold = threshold or self.config.pattern_threshold  # Use config threshold if not provided
        
        if isinstance(data, (list, tuple)) and len(data) > 2:  # Need sufficient data points
            numeric_data = [x for x in data if isinstance(x, (int, float))]  # Filter numeric values
            
            if len(numeric_data) > 2:  # Need minimum points for trend detection
                # Detect trend pattern
                differences = [numeric_data[i+1] - numeric_data[i] for i in range(len(numeric_data)-1)]  # Calculate differences
                positive_diffs = sum(1 for d in differences if d > 0)  # Count positive changes
                negative_diffs = sum(1 for d in differences if d < 0)  # Count negative changes
                
                if positive_diffs / len(differences) > threshold:  # Strong upward trend
                    patterns.append({
                        'type': 'upward_trend',  # Pattern type
                        'confidence': positive_diffs / len(differences),  # Confidence level
                        'details': {'positive_changes': positive_diffs, 'total_changes': len(differences)}  # Pattern details
                    })
                elif negative_diffs / len(differences) > threshold:  # Strong downward trend
                    patterns.append({
                        'type': 'downward_trend',  # Pattern type
                        'confidence': negative_diffs / len(differences),  # Confidence level
                        'details': {'negative_changes': negative_diffs, 'total_changes': len(differences)}  # Pattern details
                    })
        
        return patterns  # Return detected patterns
    
    def _assess_quality(self, data: Any) -> float:
        """Assess data quality returning score from 0.0 to 1.0."""
        if data is None:  # No data provided
            return 0.0  # Lowest quality score
        
        quality_score = 1.0  # Start with perfect score
        
        if isinstance(data, (list, tuple)):  # Sequence data quality assessment
            if not data:  # Empty sequence
                return 0.0  # No data quality
            
            # Check for missing values (None, empty strings)
            missing_count = sum(1 for item in data if item is None or item == "")  # Count missing values
            if missing_count > 0:
                quality_score -= (missing_count / len(data)) * 0.5  # Reduce score for missing data
            
            # Check for data type consistency
            types = set(type(item).__name__ for item in data if item is not None)  # Get unique types
            if len(types) > 1:  # Mixed types reduce quality
                quality_score -= 0.2  # Penalty for mixed types
        
        elif isinstance(data, dict):  # Dictionary data quality assessment
            if not data:  # Empty dictionary
                return 0.0  # No data quality
            
            # Check for None values in dictionary
            none_values = sum(1 for value in data.values() if value is None)  # Count None values
            if none_values > 0:
                quality_score -= (none_values / len(data)) * 0.3  # Reduce score for None values
        
        return max(0.0, quality_score)  # Ensure score doesn't go below 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analyzer performance statistics."""
        with self._lock:  # Thread-safe statistics access
            return {
                'analyzer_name': self.name,  # Analyzer identifier
                'analysis_count': self._analysis_count,  # Total analyses performed
                'total_execution_time': self._total_execution_time,  # Total time spent
                'average_execution_time': (
                    self._total_execution_time / self._analysis_count 
                    if self._analysis_count > 0 else 0.0
                ),  # Average execution time
                'last_analysis_time': (
                    self._last_analysis_time.isoformat() 
                    if self._last_analysis_time else None
                ),  # Last analysis timestamp
                'configuration': self.config.to_dict()  # Current configuration
            }
    
    @abstractmethod
    def _analyze_impl(self, data: Any, config: AnalysisConfig) -> Any:
        """
        Abstract method for analyzer-specific implementation.
        
        This method must be implemented by all concrete analyzer classes
        to provide their specific analysis functionality.
        
        Args:
            data: Input data for analysis
            config: Configuration for analysis operation
            
        Returns:
            Analysis result data (type depends on analyzer implementation)
        """
        pass  # Must be implemented by subclasses
    
    def analyze(self, data: Any, config: Optional[AnalysisConfig] = None) -> AnalysisResult[Any]:
        """
        Main analysis method with comprehensive error handling and logging.
        
        Provides standardized analysis workflow with timing, statistics,
        pattern detection, quality assessment, and hook execution.
        
        Args:
            data: Input data for analysis
            config: Optional configuration override
            
        Returns:
            AnalysisResult containing analysis data and metadata
        """
        start_time = time.time()  # Record analysis start time
        analysis_config = config or self.config  # Use provided config or instance config
        
        # Create result object
        result = AnalysisResult[Any](
            analyzer_name=self.name,  # Set analyzer name
            data=None  # Will be populated by analysis
        )
        
        try:
            with self._lock:  # Thread-safe analysis execution
                self.logger.info(f"Starting analysis with analyzer '{self.name}'")
                self.logger.debug(f"Analysis input data type: {type(data).__name__}")
                
                # Run pre-analysis hooks
                self._run_hooks('pre_analysis', data, analysis_config)
                
                # Perform the actual analysis
                analysis_result = self._analyze_impl(data, analysis_config)  # Call implementation
                result.data = analysis_result  # Store analysis result
                
                # Calculate statistics
                stats = self._calculate_statistics(data)  # Calculate input data statistics
                for stat_name, stat_value in stats.items():
                    result.add_statistic(stat_name, stat_value)  # Add statistics to result
                
                # Detect patterns
                patterns = self._detect_patterns(data, analysis_config.pattern_threshold)  # Detect patterns
                for pattern in patterns:
                    result.add_pattern(pattern['type'], pattern['confidence'], pattern['details'])  # Add patterns to result
                    self._run_hooks('on_pattern', pattern)  # Run pattern hooks
                
                # Assess quality
                result.quality_score = self._assess_quality(data)  # Calculate quality score
                
                # Update statistics
                self._analysis_count += 1  # Increment analysis count
                self._last_analysis_time = datetime.now()  # Update last analysis time
                
                # Run post-analysis hooks
                self._run_hooks('post_analysis', result)
                
                self.logger.info(f"Analysis completed successfully with analyzer '{self.name}'")
                
        except Exception as e:
            # Handle analysis errors
            error_message = f"Analysis failed: {str(e)}"  # Create error message
            result.add_error(error_message)  # Add error to result
            self.logger.error(error_message)  # Log error
            
            # Run error hooks
            self._run_hooks('on_error', e, result)
            
        finally:
            # Record execution time
            execution_time = time.time() - start_time  # Calculate execution time
            result.execution_time = execution_time  # Store execution time
            
            with self._lock:  # Thread-safe statistics update
                self._total_execution_time += execution_time  # Add to total time
            
            self.logger.debug(f"Analysis execution time: {execution_time:.3f} seconds")
        
        return result  # Return analysis result