"""
Comprehensive Test Suite for Analysis Framework

This module provides complete test coverage for the consolidated analysis
framework including unit tests, integration tests, and performance tests
for all analysis components.

Test Categories:
    - BaseAnalyzerV2 core functionality
    - AnalysisResult and AnalysisConfig classes
    - EnhancedSummarizer analysis capabilities
    - Registry system and analyzer discovery
    - Threading and thread safety
    - Error handling and edge cases
    - Integration with Context and Scriptlet frameworks

Features:
    - Comprehensive test coverage with fixtures
    - Mock data generation for testing
    - Performance benchmarking
    - Thread safety validation
    - Integration testing with other frameworks
"""

import pytest
import threading
import time
import json
from typing import Dict, Any, List
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import analysis framework components
from src.analysis.framework import (
    BaseAnalyzerV2, AnalysisResult, AnalysisConfig, AnalysisError
)
from src.analysis.components import (
    EnhancedSummarizer, StatisticalAnalyzer, PatternAnalyzer, QualityAnalyzer
)
from src.analysis.registry import (
    AnalysisRegistry, register_analyzer, AnalyzerFactory, get_available_analyzers
)


class TestAnalysisConfig:
    """Test suite for AnalysisConfig class."""
    
    def test_default_config_creation(self):
        """Test creation of AnalysisConfig with default values."""
        config = AnalysisConfig()  # Create default config
        
        # Verify default values
        assert config.timeout_seconds == 300  # Default timeout
        assert config.enable_threading is True  # Threading enabled by default
        assert config.max_memory_mb == 512  # Default memory limit
        assert config.statistical_precision == 6  # Default precision
        assert config.pattern_threshold == 0.7  # Default pattern threshold
        assert config.quality_threshold == 0.8  # Default quality threshold
        assert config.include_raw_data is False  # Raw data not included by default
        assert config.format_output is True  # Output formatting enabled
        assert config.save_intermediate is False  # Intermediate saving disabled
        assert isinstance(config.pre_analysis_hooks, list)  # Hooks as list
        assert isinstance(config.post_analysis_hooks, list)  # Hooks as list
    
    def test_config_with_custom_values(self):
        """Test AnalysisConfig with custom values."""
        config = AnalysisConfig(
            timeout_seconds=600,  # Custom timeout
            enable_threading=False,  # Disable threading
            max_memory_mb=1024,  # Custom memory limit
            debug_mode=True,  # Enable debug
            statistical_precision=8,  # Higher precision
            include_raw_data=True,  # Include raw data
            pre_analysis_hooks=['hook1', 'hook2']  # Custom hooks
        )
        
        # Verify custom values
        assert config.timeout_seconds == 600  # Custom timeout set
        assert config.enable_threading is False  # Threading disabled
        assert config.max_memory_mb == 1024  # Custom memory limit set
        assert config.debug_mode is True  # Debug mode enabled
        assert config.statistical_precision == 8  # Higher precision set
        assert config.include_raw_data is True  # Raw data included
        assert config.pre_analysis_hooks == ['hook1', 'hook2']  # Custom hooks set
    
    def test_config_to_dict_conversion(self):
        """Test conversion of AnalysisConfig to dictionary."""
        config = AnalysisConfig(timeout_seconds=600, debug_mode=True)  # Create config
        config_dict = config.to_dict()  # Convert to dictionary
        
        # Verify dictionary structure
        assert isinstance(config_dict, dict)  # Should be dictionary
        assert config_dict['timeout_seconds'] == 600  # Custom value preserved
        assert config_dict['debug_mode'] is True  # Debug mode preserved
        assert 'enable_threading' in config_dict  # Required field present
        assert 'max_memory_mb' in config_dict  # Required field present
    
    def test_config_from_dict_creation(self):
        """Test creation of AnalysisConfig from dictionary."""
        config_dict = {
            'timeout_seconds': 900,  # Custom timeout
            'enable_threading': False,  # Disable threading
            'debug_mode': True,  # Enable debug
            'statistical_precision': 4  # Lower precision
        }
        
        config = AnalysisConfig.from_dict(config_dict)  # Create from dict
        
        # Verify values from dictionary
        assert config.timeout_seconds == 900  # Value from dict
        assert config.enable_threading is False  # Value from dict
        assert config.debug_mode is True  # Value from dict
        assert config.statistical_precision == 4  # Value from dict
    
    def test_config_from_dict_with_invalid_keys(self):
        """Test AnalysisConfig creation from dict with invalid keys."""
        config_dict = {
            'timeout_seconds': 300,  # Valid key
            'invalid_key': 'invalid_value',  # Invalid key
            'another_invalid': 123  # Another invalid key
        }
        
        config = AnalysisConfig.from_dict(config_dict)  # Should filter invalid keys
        
        # Verify valid keys are processed, invalid keys ignored
        assert config.timeout_seconds == 300  # Valid key processed
        assert not hasattr(config, 'invalid_key')  # Invalid key not set
        assert not hasattr(config, 'another_invalid')  # Invalid key not set


class TestAnalysisResult:
    """Test suite for AnalysisResult class."""
    
    def test_basic_result_creation(self):
        """Test creation of basic AnalysisResult."""
        result = AnalysisResult[Dict](
            analyzer_name="test_analyzer",  # Analyzer name
            data={"key": "value"}  # Test data
        )
        
        # Verify basic properties
        assert result.analyzer_name == "test_analyzer"  # Analyzer name set
        assert result.data == {"key": "value"}  # Data set correctly
        assert result.success is True  # Success by default
        assert result.execution_time == 0.0  # Default execution time
        assert result.memory_used == 0  # Default memory usage
        assert result.quality_score == 1.0  # Perfect quality by default
        assert isinstance(result.metadata, dict)  # Metadata is dictionary
        assert isinstance(result.statistics, dict)  # Statistics is dictionary
        assert isinstance(result.patterns, list)  # Patterns is list
        assert isinstance(result.errors, list)  # Errors is list
        assert isinstance(result.warnings, list)  # Warnings is list
        assert isinstance(result.created_at, datetime)  # Created timestamp exists
    
    def test_result_error_handling(self):
        """Test error handling in AnalysisResult."""
        result = AnalysisResult[str](analyzer_name="test", data="test_data")  # Create result
        
        # Add error
        result.add_error("Test error message")  # Add error
        
        # Verify error handling
        assert result.success is False  # Success flag changed
        assert "Test error message" in result.errors  # Error added to list
        assert len(result.errors) == 1  # Correct error count
    
    def test_result_warning_handling(self):
        """Test warning handling in AnalysisResult."""
        result = AnalysisResult[str](analyzer_name="test", data="test_data")  # Create result
        
        # Add warnings
        result.add_warning("First warning")  # Add warning
        result.add_warning("Second warning")  # Add another warning
        
        # Verify warning handling
        assert result.success is True  # Warnings don't affect success
        assert "First warning" in result.warnings  # First warning added
        assert "Second warning" in result.warnings  # Second warning added
        assert len(result.warnings) == 2  # Correct warning count
    
    def test_result_statistics_management(self):
        """Test statistics management in AnalysisResult."""
        result = AnalysisResult[List](analyzer_name="test", data=[1, 2, 3])  # Create result
        
        # Add statistics
        result.add_statistic("mean", 2.0)  # Add mean statistic
        result.add_statistic("std_dev", 0.816)  # Add standard deviation
        
        # Verify statistics
        assert result.statistics["mean"] == 2.0  # Mean statistic stored
        assert result.statistics["std_dev"] == 0.816  # Standard deviation stored
        assert len(result.statistics) == 2  # Correct statistic count
    
    def test_result_pattern_management(self):
        """Test pattern management in AnalysisResult."""
        result = AnalysisResult[List](analyzer_name="test", data=[1, 2, 3, 4])  # Create result
        
        # Add pattern
        result.add_pattern("upward_trend", 0.95, {"slope": 1.0})  # Add pattern
        
        # Verify pattern
        assert len(result.patterns) == 1  # One pattern added
        pattern = result.patterns[0]  # Get first pattern
        assert pattern["type"] == "upward_trend"  # Pattern type correct
        assert pattern["confidence"] == 0.95  # Confidence correct
        assert pattern["details"]["slope"] == 1.0  # Details correct
        assert "detected_at" in pattern  # Timestamp added
    
    def test_result_to_dict_conversion(self):
        """Test AnalysisResult conversion to dictionary."""
        result = AnalysisResult[Dict](
            analyzer_name="test_analyzer",  # Analyzer name
            data={"test": "data"}  # Test data
        )
        
        # Add some data
        result.add_error("Test error")  # Add error
        result.add_warning("Test warning")  # Add warning
        result.add_statistic("count", 10)  # Add statistic
        result.add_pattern("test_pattern", 0.8, {"info": "test"})  # Add pattern
        
        # Convert to dictionary
        result_dict = result.to_dict()  # Convert to dict
        
        # Verify dictionary structure
        assert isinstance(result_dict, dict)  # Should be dictionary
        assert result_dict["analyzer_name"] == "test_analyzer"  # Analyzer name preserved
        assert result_dict["data"] == {"test": "data"}  # Data preserved
        assert result_dict["success"] is False  # Success affected by error
        assert "Test error" in result_dict["errors"]  # Error preserved
        assert "Test warning" in result_dict["warnings"]  # Warning preserved
        assert result_dict["statistics"]["count"] == 10  # Statistic preserved
        assert len(result_dict["patterns"]) == 1  # Pattern preserved
        assert isinstance(result_dict["created_at"], str)  # Timestamp as ISO string


class MockAnalyzer(BaseAnalyzerV2):
    """Mock analyzer for testing BaseAnalyzerV2 functionality."""
    
    def __init__(self, config: AnalysisConfig = None):
        """Initialize mock analyzer."""
        super().__init__("mock_analyzer", config)  # Call parent constructor with fixed name
        self.analysis_calls = []  # Track analysis calls
    
    def _analyze_impl(self, data: Any, config: AnalysisConfig) -> Any:
        """Mock implementation that records calls."""
        self.analysis_calls.append({
            'data': data,  # Input data
            'config': config.to_dict(),  # Configuration used
            'timestamp': datetime.now()  # When called
        })
        
        # Return processed data
        if isinstance(data, list):  # List processing
            return {"processed_list": len(data)}  # Return length info
        elif isinstance(data, dict):  # Dictionary processing
            return {"processed_dict": len(data)}  # Return size info
        else:  # Other data
            return {"processed_other": str(type(data))}  # Return type info


class NamedMockAnalyzer(BaseAnalyzerV2):
    """Mock analyzer that accepts name in constructor for registry testing."""
    
    _registry_name = "mock_analyzer"  # Default name for registry
    
    def __init__(self, config: AnalysisConfig = None):
        """Initialize named mock analyzer."""
        # Use class attribute for name if available, otherwise default
        analyzer_name = getattr(self.__class__, '_registry_name', 'named_mock_analyzer')
        super().__init__(analyzer_name, config)  # Call parent constructor
        self.analysis_calls = []  # Track analysis calls
        
    @classmethod
    def set_registry_name(cls, name: str) -> None:
        """Set the name to use when creating instances from registry."""
        cls._registry_name = name
    
    def _analyze_impl(self, data: Any, config: AnalysisConfig) -> Any:
        """Mock implementation that records calls."""
        self.analysis_calls.append({
            'data': data,  # Input data
            'config': config.to_dict(),  # Configuration used
            'timestamp': datetime.now()  # When called
        })
        
        # Return processed data
        if isinstance(data, list):  # List processing
            return {"processed_list": len(data)}  # Return length info
        elif isinstance(data, dict):  # Dictionary processing
            return {"processed_dict": len(data)}  # Return size info
        else:  # Other data
            return {"processed_other": str(type(data))}  # Return type info


class TestBaseAnalyzerV2:
    """Test suite for BaseAnalyzerV2 abstract base class."""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization with configuration."""
        config = AnalysisConfig(timeout_seconds=600)  # Create config
        analyzer = MockAnalyzer(config)  # Create analyzer
        
        # Verify initialization
        assert analyzer.name == "mock_analyzer"  # Name set correctly
        assert analyzer.config.timeout_seconds == 600  # Config applied
        assert hasattr(analyzer, '_lock')  # Thread lock exists
        assert hasattr(analyzer, 'logger')  # Logger exists
        assert hasattr(analyzer, '_hooks')  # Hook system exists
        assert analyzer._analysis_count == 0  # Initial count zero
        assert analyzer._total_execution_time == 0.0  # Initial time zero
    
    def test_analyzer_with_default_config(self):
        """Test analyzer initialization with default configuration."""
        analyzer = MockAnalyzer()  # Create with defaults
        
        # Verify default configuration
        assert analyzer.config.timeout_seconds == 300  # Default timeout
        assert analyzer.config.enable_threading is True  # Default threading
        assert analyzer.config.statistical_precision == 6  # Default precision
    
    def test_basic_analysis_execution(self):
        """Test basic analysis execution."""
        analyzer = MockAnalyzer()  # Create analyzer
        test_data = [1, 2, 3, 4, 5]  # Test data
        
        # Perform analysis
        result = analyzer.analyze(test_data)  # Execute analysis
        
        # Verify result
        assert isinstance(result, AnalysisResult)  # Result is correct type
        assert result.analyzer_name == "mock_analyzer"  # Analyzer name correct
        assert result.success is True  # Analysis succeeded
        assert result.data == {"processed_list": 5}  # Correct processing
        assert result.execution_time > 0  # Execution time recorded
        assert len(analyzer.analysis_calls) == 1  # Analysis call recorded
    
    def test_analysis_with_statistics_calculation(self):
        """Test analysis with automatic statistics calculation."""
        analyzer = MockAnalyzer()  # Create analyzer
        numeric_data = [10, 20, 30, 40, 50]  # Numeric test data
        
        # Perform analysis
        result = analyzer.analyze(numeric_data)  # Execute analysis
        
        # Verify statistics
        assert 'count' in result.statistics  # Count statistic present
        assert 'mean' in result.statistics  # Mean statistic present
        assert 'min' in result.statistics  # Min statistic present
        assert 'max' in result.statistics  # Max statistic present
        assert result.statistics['count'] == 5  # Correct count
        assert result.statistics['mean'] == 30.0  # Correct mean
        assert result.statistics['min'] == 10  # Correct min
        assert result.statistics['max'] == 50  # Correct max
    
    def test_pattern_detection(self):
        """Test automatic pattern detection."""
        analyzer = MockAnalyzer()  # Create analyzer
        upward_trend = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Strong upward trend
        
        # Perform analysis
        result = analyzer.analyze(upward_trend)  # Execute analysis
        
        # Verify pattern detection
        assert len(result.patterns) > 0  # Pattern detected
        pattern = result.patterns[0]  # Get first pattern
        assert pattern['type'] == 'upward_trend'  # Correct pattern type
        assert pattern['confidence'] > 0.7  # High confidence
    
    def test_quality_assessment(self):
        """Test data quality assessment."""
        analyzer = MockAnalyzer()  # Create analyzer
        
        # Test with good data
        good_data = [1, 2, 3, 4, 5]  # Clean numeric data
        result = analyzer.analyze(good_data)  # Analyze good data
        assert result.quality_score > 0.8  # High quality score
        
        # Test with poor data
        poor_data = [1, None, 3, "", 5]  # Data with missing values
        result = analyzer.analyze(poor_data)  # Analyze poor data
        assert result.quality_score < 0.8  # Lower quality score
    
    def test_hook_system(self):
        """Test analyzer hook system."""
        analyzer = MockAnalyzer()  # Create analyzer
        hook_calls = []  # Track hook calls
        
        def pre_analysis_hook(data, config):
            """Test pre-analysis hook."""
            hook_calls.append(("pre_analysis", data, config))  # Record call
        
        def post_analysis_hook(result):
            """Test post-analysis hook."""
            hook_calls.append(("post_analysis", result))  # Record call
        
        # Add hooks
        analyzer.add_hook('pre_analysis', pre_analysis_hook)  # Add pre-hook
        analyzer.add_hook('post_analysis', post_analysis_hook)  # Add post-hook
        
        # Perform analysis
        test_data = [1, 2, 3]  # Test data
        result = analyzer.analyze(test_data)  # Execute analysis with hooks
        
        # Verify hooks were called
        assert len(hook_calls) == 2  # Both hooks called
        assert hook_calls[0][0] == "pre_analysis"  # Pre-hook called first
        assert hook_calls[1][0] == "post_analysis"  # Post-hook called second
        assert hook_calls[0][1] == test_data  # Pre-hook got data
        assert hook_calls[1][1] == result  # Post-hook got result
    
    def test_error_handling(self):
        """Test error handling in analysis."""
        # Create analyzer that will fail
        class FailingAnalyzer(BaseAnalyzerV2):
            def _analyze_impl(self, data, config):
                raise ValueError("Test analysis error")  # Simulate error
        
        analyzer = FailingAnalyzer("failing_test")  # Create failing analyzer
        
        # Perform analysis that should fail
        result = analyzer.analyze([1, 2, 3])  # Execute analysis
        
        # Verify error handling
        assert result.success is False  # Analysis marked as failed
        assert len(result.errors) > 0  # Error recorded
        assert "Test analysis error" in str(result.errors)  # Error message preserved
    
    def test_analyzer_statistics_tracking(self):
        """Test analyzer performance statistics tracking."""
        analyzer = MockAnalyzer()  # Create analyzer
        
        # Perform multiple analyses
        for i in range(3):  # Multiple analysis runs
            analyzer.analyze([1, 2, 3])  # Execute analysis
            time.sleep(0.01)  # Small delay for timing
        
        # Get analyzer statistics
        stats = analyzer.get_statistics()  # Get performance stats
        
        # Verify statistics tracking
        assert stats['analyzer_name'] == "mock_analyzer"  # Correct name
        assert stats['analysis_count'] == 3  # Correct count
        assert stats['total_execution_time'] > 0  # Time recorded
        assert stats['average_execution_time'] > 0  # Average calculated
        assert stats['last_analysis_time'] is not None  # Last time recorded


class TestEnhancedSummarizer:
    """Test suite for EnhancedSummarizer analyzer."""
    
    def test_summarizer_initialization(self):
        """Test EnhancedSummarizer initialization."""
        summarizer = EnhancedSummarizer()  # Create summarizer
        
        # Verify initialization
        assert summarizer.name == "enhanced_summarizer"  # Correct name
        assert isinstance(summarizer.config, AnalysisConfig)  # Has config
    
    def test_list_data_summarization(self):
        """Test summarization of list data."""
        summarizer = EnhancedSummarizer()  # Create summarizer
        test_data = [1, 2, 3, 4, 5, "text", None]  # Mixed data
        
        # Perform summarization
        result = summarizer.analyze(test_data)  # Analyze data
        
        # Verify result structure
        assert result.success is True  # Analysis succeeded
        summary = result.data  # Get summary data
        
        # Verify summary content
        assert summary['data_type'] == 'list'  # Correct data type
        assert summary['length'] == 7  # Correct length
        assert summary['empty'] is False  # Not empty
        assert 'element_types' in summary  # Element types analyzed
        assert 'numeric_analysis' in summary  # Numeric analysis present
        assert 'missing_values' in summary  # Missing values analyzed
    
    def test_numeric_data_analysis(self):
        """Test numeric data analysis capabilities."""
        summarizer = EnhancedSummarizer()  # Create summarizer
        numeric_data = [10, 15, 20, 25, 30, 35, 40]  # Pure numeric data
        
        # Perform analysis
        result = summarizer.analyze(numeric_data)  # Analyze numeric data
        summary = result.data  # Get summary
        
        # Verify numeric analysis
        numeric_analysis = summary['numeric_analysis']  # Get numeric section
        assert numeric_analysis['count'] == 7  # Correct count
        assert numeric_analysis['mean'] == 25.0  # Correct mean
        assert numeric_analysis['median'] == 25.0  # Correct median
        assert numeric_analysis['min'] == 10  # Correct minimum
        assert numeric_analysis['max'] == 40  # Correct maximum
        assert 'std_dev' in numeric_analysis  # Standard deviation calculated
        assert 'quartiles' in numeric_analysis  # Quartiles calculated
        assert 'outliers' in numeric_analysis  # Outlier detection performed
    
    def test_string_data_analysis(self):
        """Test string data analysis capabilities."""
        summarizer = EnhancedSummarizer()  # Create summarizer
        string_data = ["hello", "world", "test", "analysis", ""]  # String data
        
        # Perform analysis
        result = summarizer.analyze(string_data)  # Analyze string data
        summary = result.data  # Get summary
        
        # Verify string analysis
        assert 'string_analysis' in summary  # String analysis present
        string_analysis = summary['string_analysis']  # Get string section
        assert string_analysis['count'] == 5  # Correct count
        assert string_analysis['empty_strings'] == 1  # Empty string detected
        assert 'character_analysis' in string_analysis  # Character analysis present
    
    def test_dictionary_data_analysis(self):
        """Test dictionary data analysis capabilities."""
        summarizer = EnhancedSummarizer()  # Create summarizer
        dict_data = {
            "name": "test",  # String value
            "count": 42,  # Numeric value
            "active": True,  # Boolean value
            "data": None  # None value
        }
        
        # Perform analysis
        result = summarizer.analyze(dict_data)  # Analyze dictionary
        summary = result.data  # Get summary
        
        # Verify dictionary analysis
        assert summary['data_type'] == 'dict'  # Correct type
        assert summary['key_count'] == 4  # Correct key count
        assert summary['empty'] is False  # Not empty
        assert 'key_types' in summary  # Key types analyzed
        assert 'value_types' in summary  # Value types analyzed
        assert 'null_values' in summary  # Null values analyzed
    
    def test_quality_assessment(self):
        """Test data quality assessment in summarizer."""
        summarizer = EnhancedSummarizer()  # Create summarizer
        
        # Test high quality data
        good_data = [1, 2, 3, 4, 5]  # Clean data
        result = summarizer.analyze(good_data)  # Analyze good data
        quality = result.data['quality_assessment']  # Get quality info
        assert quality['overall_score'] > 0.8  # High quality score
        
        # Test poor quality data
        bad_data = [1, None, "", 4, None]  # Data with issues
        result = summarizer.analyze(bad_data)  # Analyze bad data
        quality = result.data['quality_assessment']  # Get quality info
        assert quality['overall_score'] < 0.8  # Lower quality score
        assert len(quality['issues']) > 0  # Issues identified
        assert len(quality['recommendations']) > 0  # Recommendations provided
    
    def test_empty_data_handling(self):
        """Test handling of empty data."""
        summarizer = EnhancedSummarizer()  # Create summarizer
        
        # Test empty list
        result = summarizer.analyze([])  # Analyze empty list
        summary = result.data  # Get summary
        assert summary['empty'] is True  # Correctly identified as empty
        assert summary['length'] == 0  # Zero length
        
        # Test None data
        result = summarizer.analyze(None)  # Analyze None
        assert result.success is True  # Analysis completes
        quality = result.data['quality_assessment']  # Get quality
        assert quality['overall_score'] == 0.0  # Lowest quality for None


class TestAnalysisRegistry:
    """Test suite for AnalysisRegistry system."""
    
    def setup_method(self):
        """Setup for each test method."""
        # Clear registry before each test
        AnalysisRegistry.clear_registry()  # Clean start
    
    def teardown_method(self):
        """Cleanup after each test method."""
        # Clear registry after each test
        AnalysisRegistry.clear_registry()  # Clean end
    
    def test_analyzer_registration(self):
        """Test analyzer registration in registry."""
        # Register analyzer
        AnalysisRegistry.register(
            analyzer_name="test_analyzer",  # Name
            analyzer_class=MockAnalyzer,  # Class
            description="Test analyzer for unit testing",  # Description
            version="1.0.0"  # Version
        )
        
        # Verify registration
        available = AnalysisRegistry.get_available_analyzers()  # Get available
        assert "test_analyzer" in available  # Analyzer registered
        
        analyzer_info = AnalysisRegistry.get_analyzer_info("test_analyzer")  # Get info
        assert analyzer_info is not None  # Info exists
        assert analyzer_info['class'] == MockAnalyzer  # Correct class
        assert analyzer_info['description'] == "Test analyzer for unit testing"  # Correct description
        assert analyzer_info['version'] == "1.0.0"  # Correct version
    
    def test_analyzer_retrieval(self):
        """Test analyzer instance retrieval from registry."""
        # Create a custom analyzer class for this test
        class RetrievalTestAnalyzer(BaseAnalyzerV2):
            def __init__(self, config=None):
                super().__init__("retrieval_test", config)
            def _analyze_impl(self, data, config):
                return {"test": "retrieval"}
        
        # Register analyzer
        AnalysisRegistry.register("retrieval_test", RetrievalTestAnalyzer)  # Register
        
        # Retrieve analyzer instance
        analyzer = AnalysisRegistry.get_analyzer("retrieval_test")  # Get instance
        
        # Verify instance
        assert isinstance(analyzer, RetrievalTestAnalyzer)  # Correct type
        assert analyzer.name == "retrieval_test"  # Correct name
    
    def test_analyzer_unregistration(self):
        """Test analyzer removal from registry."""
        # Register and then unregister
        AnalysisRegistry.register("temp_analyzer", MockAnalyzer)  # Register
        assert "temp_analyzer" in AnalysisRegistry.get_available_analyzers()  # Verify registration
        
        success = AnalysisRegistry.unregister("temp_analyzer")  # Unregister
        assert success is True  # Unregistration successful
        assert "temp_analyzer" not in AnalysisRegistry.get_available_analyzers()  # Verify removal
    
    def test_analyzer_chain_creation(self):
        """Test creation of analyzer chains."""
        # Create custom analyzer classes for chain test
        class Chain1Analyzer(BaseAnalyzerV2):
            def __init__(self, config=None):
                super().__init__("chain_1", config)
            def _analyze_impl(self, data, config):
                return {"chain": 1}
                
        class Chain2Analyzer(BaseAnalyzerV2):
            def __init__(self, config=None):
                super().__init__("chain_2", config)
            def _analyze_impl(self, data, config):
                return {"chain": 2}
        
        # Register multiple analyzers
        AnalysisRegistry.register("chain_1", Chain1Analyzer)  # First analyzer
        AnalysisRegistry.register("chain_2", Chain2Analyzer)  # Second analyzer
        
        # Create analyzer chain
        analyzers = AnalysisRegistry.create_analyzer_chain(["chain_1", "chain_2"])  # Create chain
        
        # Verify chain
        assert len(analyzers) == 2  # Two analyzers in chain
        assert isinstance(analyzers[0], Chain1Analyzer)  # First is Chain1Analyzer
        assert isinstance(analyzers[1], Chain2Analyzer)  # Second is Chain2Analyzer
        assert analyzers[0].name == "chain_1"  # First has correct name
        assert analyzers[1].name == "chain_2"  # Second has correct name
    
    def test_register_analyzer_decorator(self):
        """Test @register_analyzer decorator."""
        
        @register_analyzer(name="decorated_analyzer", description="Decorated test analyzer")
        class DecoratedAnalyzer(BaseAnalyzerV2):
            def _analyze_impl(self, data, config):
                return {"decorated": True}  # Decorated implementation
        
        # Verify decorator registration
        available = AnalysisRegistry.get_available_analyzers()  # Get available
        assert "decorated_analyzer" in available  # Decorated analyzer registered
        
        # Verify analyzer works
        analyzer = AnalysisRegistry.get_analyzer("decorated_analyzer")  # Get instance
        result = analyzer.analyze("test")  # Test analysis
        assert result.data["decorated"] is True  # Decorated functionality works
    
    def test_registry_error_handling(self):
        """Test error handling in registry operations."""
        # Test retrieval of non-existent analyzer
        with pytest.raises(AnalysisError):  # Should raise error
            AnalysisRegistry.get_analyzer("non_existent")  # Non-existent analyzer
        
        # Test registration of invalid class
        with pytest.raises(AnalysisError):  # Should raise error
            AnalysisRegistry.register("invalid", str)  # Invalid class type


class TestThreadSafety:
    """Test suite for thread safety of analysis framework."""
    
    def test_concurrent_analysis(self):
        """Test concurrent analysis execution."""
        analyzer = MockAnalyzer()  # Create analyzer
        results = []  # Store results
        errors = []  # Store errors
        
        def worker_analysis(worker_id):
            """Worker function for concurrent analysis."""
            try:
                data = list(range(worker_id * 10, (worker_id + 1) * 10))  # Worker-specific data
                result = analyzer.analyze(data)  # Perform analysis
                results.append(result)  # Store result
            except Exception as e:
                errors.append(e)  # Store error
        
        # Create and start threads
        threads = []  # Thread list
        for i in range(5):  # 5 concurrent threads
            thread = threading.Thread(target=worker_analysis, args=(i,))  # Create thread
            threads.append(thread)  # Add to list
            thread.start()  # Start thread
        
        # Wait for all threads
        for thread in threads:  # Wait for each thread
            thread.join()  # Join thread
        
        # Verify thread safety
        assert len(errors) == 0  # No errors occurred
        assert len(results) == 5  # All analyses completed
        assert analyzer._analysis_count == 5  # Count tracked correctly
        
        # Verify each result
        for result in results:  # Check each result
            assert result.success is True  # Analysis succeeded
            assert isinstance(result.data, dict)  # Correct data type
    
    def test_concurrent_registry_operations(self):
        """Test concurrent registry operations."""
        AnalysisRegistry.clear_registry()  # Start clean
        registration_errors = []  # Store registration errors
        
        def register_worker(worker_id):
            """Worker function for concurrent registration."""
            try:
                analyzer_name = f"concurrent_analyzer_{worker_id}"  # Unique name
                AnalysisRegistry.register(analyzer_name, MockAnalyzer)  # Register
            except Exception as e:
                registration_errors.append(e)  # Store error
        
        # Create and start registration threads
        threads = []  # Thread list
        for i in range(10):  # 10 concurrent registrations
            thread = threading.Thread(target=register_worker, args=(i,))  # Create thread
            threads.append(thread)  # Add to list
            thread.start()  # Start thread
        
        # Wait for all threads
        for thread in threads:  # Wait for each thread
            thread.join()  # Join thread
        
        # Verify concurrent registration
        assert len(registration_errors) == 0  # No registration errors
        available = AnalysisRegistry.get_available_analyzers()  # Get available
        assert len(available) == 10  # All analyzers registered


class TestIntegration:
    """Integration tests with other framework components."""
    
    def test_analysis_with_context_system(self):
        """Test analysis framework integration with Context system."""
        # This would test integration with the Context system
        # Implementation depends on Context system API
        pass  # Placeholder for context integration
    
    def test_analysis_with_scriptlet_framework(self):
        """Test analysis framework integration with Scriptlet framework."""  
        # This would test integration with the Scriptlet framework
        # Implementation depends on Scriptlet framework API
        pass  # Placeholder for scriptlet integration


if __name__ == "__main__":
    pytest.main([__file__, "-v"])  # Run tests with verbose output