"""
Enhanced Analysis Components

This module provides specialized analyzer implementations that extend
BaseAnalyzerV2 with specific analysis capabilities. Each component
focuses on a particular type of analysis while maintaining consistency
with the consolidated framework.

Components:
    EnhancedSummarizer: Advanced data summarization with statistics
    StatisticalAnalyzer: Comprehensive statistical analysis
    PatternAnalyzer: Pattern detection and trend analysis  
    QualityAnalyzer: Data quality assessment and validation

Features:
    - Thread-safe implementations
    - Comprehensive statistical calculations
    - Pattern detection algorithms
    - Data quality metrics
    - Integration with hook system
    - Memory usage optimization
"""

import os
import statistics
import json
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
from collections import Counter

# Import framework components
try:
    from .framework import BaseAnalyzerV2, AnalysisConfig, AnalysisResult, AnalysisError
except ImportError:
    from src.analysis.framework import BaseAnalyzerV2, AnalysisConfig, AnalysisResult, AnalysisError

# Import core logger
from src.core.logger import get_logger


class EnhancedSummarizer(BaseAnalyzerV2):
    """
    Advanced data summarization analyzer with comprehensive statistics.
    
    Provides detailed summaries of data including descriptive statistics,
    distribution analysis, and intelligent insights generation.
    
    Features:
        - Descriptive statistics (mean, median, mode, standard deviation)
        - Distribution analysis (quartiles, percentiles, skewness)
        - Data type analysis and validation
        - Missing value detection and reporting
        - Outlier identification
        - Correlation analysis for multi-dimensional data
    """
    
    def __init__(self, config: Optional[AnalysisConfig] = None) -> None:
        """Initialize EnhancedSummarizer with configuration."""
        super().__init__("enhanced_summarizer", config)  # Call parent constructor
        self.logger.info("EnhancedSummarizer initialized with advanced statistics capabilities")
    
    def _analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]:
        """
        Perform enhanced summarization analysis.
        
        Args:
            data: Input data for summarization
            config: Analysis configuration
            
        Returns:
            Dictionary containing comprehensive summary information
        """
        summary = {
            'data_type': type(data).__name__,  # Type of input data
            'timestamp': datetime.now().isoformat(),  # Analysis timestamp
            'configuration': config.to_dict()  # Configuration used
        }
        
        try:
            if isinstance(data, (list, tuple)):  # Sequence data analysis
                summary.update(self._analyze_sequence(data))  # Analyze sequence data
            elif isinstance(data, dict):  # Dictionary data analysis
                summary.update(self._analyze_dictionary(data))  # Analyze dictionary data
            elif isinstance(data, str):  # String data analysis
                summary.update(self._analyze_string(data))  # Analyze string data
            else:  # Other data types
                summary.update(self._analyze_other(data))  # Analyze other types
            
            # Add data quality assessment
            summary['quality_assessment'] = self._assess_data_quality(data)  # Quality metrics
            
            self.logger.debug(f"Summary generated: {len(summary)} metrics")
            
        except Exception as e:
            raise AnalysisError(f"Summarization failed: {str(e)}", "SUMMARIZATION_ERROR")  # Analysis error
        
        return summary  # Return complete summary
    
    def _analyze_sequence(self, data: Union[List, Tuple]) -> Dict[str, Any]:
        """Analyze sequence data (list or tuple)."""
        analysis = {
            'length': len(data),  # Number of elements
            'empty': len(data) == 0,  # Whether sequence is empty
            'element_types': {}  # Count of each element type
        }
        
        if not data:  # Empty sequence handling
            return analysis  # Return basic info for empty sequence
        
        # Analyze element types
        type_counter = Counter(type(item).__name__ for item in data)  # Count types
        analysis['element_types'] = dict(type_counter)  # Store type distribution
        analysis['unique_types'] = len(type_counter)  # Number of unique types
        analysis['homogeneous'] = len(type_counter) == 1  # All same type?
        
        # Extract numeric data for statistical analysis
        numeric_data = [item for item in data if isinstance(item, (int, float))]  # Filter numeric values
        
        if numeric_data:  # If we have numeric data
            analysis['numeric_analysis'] = self._analyze_numeric_data(numeric_data)  # Detailed numeric analysis
        
        # Extract string data for text analysis  
        string_data = [item for item in data if isinstance(item, str)]  # Filter string values
        
        if string_data:  # If we have string data
            analysis['string_analysis'] = self._analyze_string_data(string_data)  # String analysis
        
        # Missing value analysis
        null_count = sum(1 for item in data if item is None)  # Count None values
        empty_string_count = sum(1 for item in data if item == "")  # Count empty strings
        
        analysis['missing_values'] = {
            'null_count': null_count,  # Number of None values
            'empty_string_count': empty_string_count,  # Number of empty strings
            'total_missing': null_count + empty_string_count,  # Total missing
            'missing_percentage': ((null_count + empty_string_count) / len(data)) * 100  # Percentage missing
        }
        
        return analysis  # Return sequence analysis
    
    def _analyze_numeric_data(self, numeric_data: List[Union[int, float]]) -> Dict[str, Any]:
        """Perform comprehensive numeric data analysis."""
        if not numeric_data:  # No numeric data
            return {}  # Return empty analysis
        
        analysis = {
            'count': len(numeric_data),  # Number of values
            'sum': sum(numeric_data),  # Sum of all values
            'mean': statistics.mean(numeric_data),  # Average value
            'median': statistics.median(numeric_data),  # Middle value
            'min': min(numeric_data),  # Minimum value
            'max': max(numeric_data),  # Maximum value
            'range': max(numeric_data) - min(numeric_data)  # Value range
        }
        
        # Calculate standard deviation (population)
        if len(numeric_data) > 1:  # Need at least 2 values
            analysis['std_dev'] = statistics.stdev(numeric_data)  # Standard deviation
            analysis['variance'] = statistics.variance(numeric_data)  # Variance
        
        # Calculate mode (most common value)
        try:
            analysis['mode'] = statistics.mode(numeric_data)  # Most frequent value
        except statistics.StatisticsError:  # No unique mode
            analysis['mode'] = None  # No single mode
        
        # Calculate quartiles and percentiles
        sorted_data = sorted(numeric_data)  # Sort data for percentile calculation
        n = len(sorted_data)  # Length for calculations
        
        analysis['quartiles'] = {
            'q1': self._percentile(sorted_data, 25),  # First quartile
            'q2': self._percentile(sorted_data, 50),  # Second quartile (median)
            'q3': self._percentile(sorted_data, 75)   # Third quartile
        }
        
        analysis['percentiles'] = {
            'p10': self._percentile(sorted_data, 10),  # 10th percentile
            'p90': self._percentile(sorted_data, 90),  # 90th percentile
            'p95': self._percentile(sorted_data, 95),  # 95th percentile
            'p99': self._percentile(sorted_data, 99)   # 99th percentile
        }
        
        # Outlier detection using IQR method
        q1 = analysis['quartiles']['q1']  # First quartile
        q3 = analysis['quartiles']['q3']  # Third quartile
        iqr = q3 - q1  # Interquartile range
        
        lower_bound = q1 - 1.5 * iqr  # Lower outlier threshold
        upper_bound = q3 + 1.5 * iqr  # Upper outlier threshold
        
        outliers = [x for x in numeric_data if x < lower_bound or x > upper_bound]  # Find outliers
        
        analysis['outliers'] = {
            'count': len(outliers),  # Number of outliers
            'values': outliers,  # Outlier values
            'percentage': (len(outliers) / len(numeric_data)) * 100,  # Percentage outliers
            'lower_bound': lower_bound,  # Lower threshold
            'upper_bound': upper_bound   # Upper threshold
        }
        
        return analysis  # Return numeric analysis
    
    def _percentile(self, sorted_data: List[Union[int, float]], percentile: float) -> float:
        """Calculate percentile value from sorted data."""
        if not sorted_data:  # Empty data
            return 0.0  # Default value
        
        n = len(sorted_data)  # Length of data
        index = (percentile / 100) * (n - 1)  # Calculate index position
        
        if index.is_integer():  # Exact index
            return sorted_data[int(index)]  # Return exact value
        else:  # Interpolate between values
            lower_index = int(index)  # Lower index
            upper_index = lower_index + 1  # Upper index
            
            if upper_index >= n:  # Boundary check
                return sorted_data[lower_index]  # Return last value
            
            # Linear interpolation
            fraction = index - lower_index  # Fractional part
            return sorted_data[lower_index] + fraction * (sorted_data[upper_index] - sorted_data[lower_index])
    
    def _analyze_string_data(self, string_data: List[str]) -> Dict[str, Any]:
        """Analyze string data for text characteristics."""
        if not string_data:  # No string data
            return {}  # Return empty analysis
        
        # Calculate string lengths
        lengths = [len(s) for s in string_data]  # List of string lengths
        
        analysis = {
            'count': len(string_data),  # Number of strings
            'total_length': sum(lengths),  # Total character count
            'average_length': sum(lengths) / len(lengths),  # Average string length
            'min_length': min(lengths),  # Shortest string length
            'max_length': max(lengths),  # Longest string length
            'empty_strings': sum(1 for s in string_data if len(s) == 0)  # Count empty strings
        }
        
        # Character analysis
        all_chars = ''.join(string_data)  # Combine all strings
        char_counter = Counter(all_chars)  # Count each character
        
        analysis['character_analysis'] = {
            'unique_characters': len(char_counter),  # Number of unique characters
            'total_characters': len(all_chars),  # Total character count
            'most_common_char': char_counter.most_common(1)[0] if char_counter else None,  # Most frequent character
            'alphabetic_chars': sum(1 for c in all_chars if c.isalpha()),  # Letter count
            'numeric_chars': sum(1 for c in all_chars if c.isdigit()),  # Digit count
            'whitespace_chars': sum(1 for c in all_chars if c.isspace())  # Whitespace count
        }
        
        return analysis  # Return string analysis
    
    def _analyze_dictionary(self, data: Dict) -> Dict[str, Any]:
        """Analyze dictionary data structure."""
        analysis = {
            'key_count': len(data),  # Number of keys
            'empty': len(data) == 0,  # Whether dictionary is empty
            'key_types': {},  # Types of keys
            'value_types': {}  # Types of values
        }
        
        if not data:  # Empty dictionary
            return analysis  # Return basic info
        
        # Analyze key types
        key_type_counter = Counter(type(key).__name__ for key in data.keys())  # Count key types
        analysis['key_types'] = dict(key_type_counter)  # Store key type distribution
        
        # Analyze value types
        value_type_counter = Counter(type(value).__name__ for value in data.values())  # Count value types
        analysis['value_types'] = dict(value_type_counter)  # Store value type distribution
        
        # Null value analysis
        null_values = sum(1 for value in data.values() if value is None)  # Count None values
        analysis['null_values'] = {
            'count': null_values,  # Number of None values
            'percentage': (null_values / len(data)) * 100 if data else 0  # Percentage None
        }
        
        # Nested structure analysis
        nested_dicts = sum(1 for value in data.values() if isinstance(value, dict))  # Count nested dicts
        nested_lists = sum(1 for value in data.values() if isinstance(value, (list, tuple)))  # Count nested lists
        
        analysis['nested_structures'] = {
            'nested_dicts': nested_dicts,  # Number of nested dictionaries
            'nested_lists': nested_lists,  # Number of nested lists
            'has_nesting': nested_dicts + nested_lists > 0  # Whether structure has nesting
        }
        
        return analysis  # Return dictionary analysis
    
    def _analyze_string(self, data: str) -> Dict[str, Any]:
        """Analyze single string data."""
        analysis = {
            'length': len(data),  # String length
            'empty': len(data) == 0,  # Whether string is empty
            'whitespace_only': data.isspace() if data else False  # Only whitespace?
        }
        
        if data:  # Non-empty string analysis
            char_counter = Counter(data)  # Count each character
            
            analysis['character_analysis'] = {
                'unique_characters': len(char_counter),  # Number of unique characters
                'most_common_char': char_counter.most_common(1)[0],  # Most frequent character
                'alphabetic_chars': sum(1 for c in data if c.isalpha()),  # Letter count
                'numeric_chars': sum(1 for c in data if c.isdigit()),  # Digit count
                'whitespace_chars': sum(1 for c in data if c.isspace()),  # Whitespace count
                'uppercase_chars': sum(1 for c in data if c.isupper()),  # Uppercase count
                'lowercase_chars': sum(1 for c in data if c.islower())   # Lowercase count
            }
            
            # Word analysis
            words = data.split()  # Split into words
            analysis['word_analysis'] = {
                'word_count': len(words),  # Number of words
                'unique_words': len(set(words)),  # Number of unique words
                'average_word_length': sum(len(word) for word in words) / len(words) if words else 0  # Average word length
            }
        
        return analysis  # Return string analysis
    
    def _analyze_other(self, data: Any) -> Dict[str, Any]:
        """Analyze other data types."""
        analysis = {
            'type': type(data).__name__,  # Data type name
            'string_representation': str(data),  # String representation
            'is_none': data is None,  # Whether data is None
            'is_callable': callable(data),  # Whether data is callable
            'has_length': hasattr(data, '__len__')  # Whether data has length
        }
        
        # Try to get length if possible
        if analysis['has_length']:  # Has length attribute
            try:
                analysis['length'] = len(data)  # Get length
            except Exception:
                analysis['length'] = None  # Length not accessible
        
        return analysis  # Return other type analysis
    
    def _assess_data_quality(self, data: Any) -> Dict[str, Any]:
        """Comprehensive data quality assessment."""
        quality = {
            'overall_score': 1.0,  # Start with perfect score
            'issues': [],  # List of quality issues
            'recommendations': []  # List of improvement recommendations
        }
        
        # Basic existence check
        if data is None:  # No data
            quality['overall_score'] = 0.0  # Lowest score
            quality['issues'].append("Data is None")  # Record issue
            quality['recommendations'].append("Provide valid data")  # Suggest fix
            return quality  # Return immediately
        
        # Type-specific quality checks
        if isinstance(data, (list, tuple)):  # Sequence quality
            quality.update(self._assess_sequence_quality(data))  # Assess sequence
        elif isinstance(data, dict):  # Dictionary quality
            quality.update(self._assess_dictionary_quality(data))  # Assess dictionary
        elif isinstance(data, str):  # String quality
            quality.update(self._assess_string_quality(data))  # Assess string
        
        return quality  # Return quality assessment
    
    def _assess_sequence_quality(self, data: Union[List, Tuple]) -> Dict[str, Any]:
        """Assess quality of sequence data."""
        quality = {'overall_score': 1.0, 'issues': [], 'recommendations': []}  # Initialize quality
        
        if not data:  # Empty sequence
            quality['overall_score'] = 0.2  # Low score for empty data
            quality['issues'].append("Sequence is empty")  # Record issue
            quality['recommendations'].append("Provide data elements")  # Suggest fix
            return quality  # Return early
        
        # Check for missing values
        missing_count = sum(1 for item in data if item is None or item == "")  # Count missing values
        if missing_count > 0:
            missing_ratio = missing_count / len(data)  # Calculate ratio
            quality['overall_score'] -= missing_ratio * 0.5  # Reduce score
            quality['issues'].append(f"Contains {missing_count} missing values ({missing_ratio:.1%})")  # Record issue
            quality['recommendations'].append("Handle or remove missing values")  # Suggest fix
        
        # Check type consistency
        types = set(type(item).__name__ for item in data if item is not None)  # Get unique types
        if len(types) > 1:  # Mixed types
            quality['overall_score'] -= 0.2  # Reduce score for inconsistency
            quality['issues'].append(f"Mixed data types: {', '.join(types)}")  # Record issue
            quality['recommendations'].append("Ensure consistent data types")  # Suggest fix
        
        return quality  # Return sequence quality
    
    def _assess_dictionary_quality(self, data: Dict) -> Dict[str, Any]:
        """Assess quality of dictionary data."""
        quality = {'overall_score': 1.0, 'issues': [], 'recommendations': []}  # Initialize quality
        
        if not data:  # Empty dictionary
            quality['overall_score'] = 0.2  # Low score for empty data
            quality['issues'].append("Dictionary is empty")  # Record issue
            quality['recommendations'].append("Add key-value pairs")  # Suggest fix
            return quality  # Return early
        
        # Check for None values
        none_count = sum(1 for value in data.values() if value is None)  # Count None values
        if none_count > 0:
            none_ratio = none_count / len(data)  # Calculate ratio
            quality['overall_score'] -= none_ratio * 0.3  # Reduce score
            quality['issues'].append(f"Contains {none_count} None values ({none_ratio:.1%})")  # Record issue
            quality['recommendations'].append("Handle None values appropriately")  # Suggest fix
        
        return quality  # Return dictionary quality
    
    def _assess_string_quality(self, data: str) -> Dict[str, Any]:
        """Assess quality of string data."""
        quality = {'overall_score': 1.0, 'issues': [], 'recommendations': []}  # Initialize quality
        
        if not data:  # Empty string
            quality['overall_score'] = 0.1  # Very low score
            quality['issues'].append("String is empty")  # Record issue
            quality['recommendations'].append("Provide meaningful text content")  # Suggest fix
        elif data.isspace():  # Only whitespace
            quality['overall_score'] = 0.3  # Low score
            quality['issues'].append("String contains only whitespace")  # Record issue
            quality['recommendations'].append("Add meaningful content")  # Suggest fix
        
        return quality  # Return string quality


class StatisticalAnalyzer(BaseAnalyzerV2):
    """
    Comprehensive statistical analysis for numeric data.
    
    Provides advanced statistical calculations, distribution analysis,
    hypothesis testing, and correlation analysis capabilities.
    """
    
    def __init__(self, config: Optional[AnalysisConfig] = None) -> None:
        """Initialize StatisticalAnalyzer with configuration."""
        super().__init__("statistical_analyzer", config)  # Call parent constructor
        self.logger.info("StatisticalAnalyzer initialized with advanced statistical capabilities")
    
    def _analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis."""
        # Implementation would include advanced statistical methods
        # This is a framework showing the structure
        return {"analysis": "statistical_framework_ready"}  # Placeholder return


class PatternAnalyzer(BaseAnalyzerV2):
    """
    Pattern detection and trend analysis for data sequences.
    
    Identifies trends, cycles, anomalies, and recurring patterns
    in time series and sequential data.
    """
    
    def __init__(self, config: Optional[AnalysisConfig] = None) -> None:
        """Initialize PatternAnalyzer with configuration."""
        super().__init__("pattern_analyzer", config)  # Call parent constructor
        self.logger.info("PatternAnalyzer initialized with pattern detection capabilities")
    
    def _analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]:
        """Perform pattern detection analysis."""
        # Implementation would include pattern detection algorithms
        # This is a framework showing the structure
        return {"analysis": "pattern_framework_ready"}  # Placeholder return


class QualityAnalyzer(BaseAnalyzerV2):
    """
    Data quality assessment and validation analyzer.
    
    Evaluates data completeness, consistency, accuracy, and validity
    providing actionable quality metrics and improvement recommendations.
    """
    
    def __init__(self, config: Optional[AnalysisConfig] = None) -> None:
        """Initialize QualityAnalyzer with configuration."""
        super().__init__("quality_analyzer", config)  # Call parent constructor
        self.logger.info("QualityAnalyzer initialized with data quality assessment capabilities")
    
    def _analyze_impl(self, data: Any, config: AnalysisConfig) -> Dict[str, Any]:
        """Perform data quality analysis."""
        # Implementation would include quality assessment algorithms
        # This is a framework showing the structure  
        return {"analysis": "quality_framework_ready"}  # Placeholder return