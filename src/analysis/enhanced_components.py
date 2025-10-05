"""
Enhanced Analysis Components with Context Integration

This module provides enhanced analyzer implementations that integrate with
the Context system and provide advanced features for Framework0.

Components:
    ContextAwareSummarizer: Advanced summarizer with Context integration
    MetricsAnalyzer: Comprehensive metrics analysis with Context tracking
    DependencyAnalyzer: Analyzer dependency tracking and resolution
    PipelineAnalyzer: Pipeline execution management and coordination
    
Features:
    - Full Context system integration
    - Advanced dependency tracking
    - Inter-analyzer communication
    - Real-time metrics and monitoring
    - Enhanced error handling and recovery
    - Plugin architecture support
"""

import os
import time
import json
import statistics
from typing import Dict, Any, List, Optional, Union, Set, Tuple
from datetime import datetime, timedelta
from collections import Counter, defaultdict

# Import core systems
from src.core.logger import get_logger
from orchestrator.context.context import Context

# Import enhanced framework
try:
    from .enhanced_framework import (
        EnhancedAnalyzerV2,
        AsyncAnalyzerV2,
        BatchAnalyzerV2,
        DistributedAnalyzer,
        CompositeAnalyzer,
        CachingAnalyzer,
        AnalysisChain,
        AnalysisConfig,
        AnalysisResult,
        AnalysisError,
    )
except ImportError:
    from src.analysis.enhanced_framework import (
        EnhancedAnalyzerV2,
        AsyncAnalyzerV2,
        BatchAnalyzerV2,
        DistributedAnalyzer,
        CompositeAnalyzer,
        CachingAnalyzer,
        AnalysisChain,
        AnalysisConfig,
        AnalysisResult,
        AnalysisError,
    )# Import base components for compatibility
from .components import EnhancedSummarizer as BaseSummarizer


class ContextAwareSummarizer(EnhancedAnalyzerV2):
    """
    Context-aware data summarizer with advanced tracking and integration.
    
    Extends EnhancedSummarizer with Context system integration, providing
    comprehensive data summarization with full traceability and advanced
    statistical analysis capabilities.
    
    Features:
        - Context-integrated statistical analysis
        - Historical data tracking and comparison
        - Advanced pattern detection with context awareness
        - Quality assessment with context-based recommendations
        - Real-time performance monitoring
    """
    
    def __init__(self, name: str = "context_aware_summarizer", 
                 config: Optional[EnhancedAnalysisConfig] = None,
                 context: Optional[Context] = None) -> None:
        """Initialize context-aware summarizer with enhanced capabilities."""
        super().__init__(name, config, context)  # Initialize enhanced analyzer
        
        # Initialize base summarizer for core functionality
        self.base_summarizer = BaseSummarizer()  # Base summarization logic
        
        # Context-aware features
        self.summary_history: List[Dict[str, Any]] = []  # Historical summaries
        self.comparison_baselines: Dict[str, Any] = {}  # Baseline comparisons
        self.trend_tracking: Dict[str, List[float]] = defaultdict(list)  # Trend data
        
        # Performance tracking
        self.analysis_metrics = {
            'total_analyses': 0,  # Total number of analyses performed
            'total_data_points': 0,  # Total data points processed
            'average_processing_time': 0.0,  # Average processing time
            'cache_hit_rate': 0.0,  # Cache hit rate percentage
            'error_rate': 0.0  # Error rate percentage
        }
        
        self.logger.info(f"ContextAwareSummarizer '{name}' initialized with Context integration")
    
    def _analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]:
        """
        Perform context-aware summarization analysis.
        
        Args:
            data: Input data for summarization
            config: Enhanced analysis configuration
            
        Returns:
            Dictionary containing comprehensive summary with context integration
        """
        start_time = time.time()  # Record analysis start
        
        try:
            # Get base summary using existing logic
            base_summary = self.base_summarizer._analyze_impl(data, config)  # Base analysis
            
            # Enhance summary with context-aware features
            enhanced_summary = self._create_enhanced_summary(base_summary, data, config)  # Context enhancement
            
            # Store summary in context for future reference
            if config.enable_context_integration:
                self._store_summary_in_context(enhanced_summary)  # Store in context
            
            # Update performance metrics
            self._update_performance_metrics(start_time, len(str(data)))  # Update metrics
            
            # Track trends over time
            self._track_analysis_trends(enhanced_summary)  # Trend tracking
            
            return enhanced_summary  # Return enhanced summary
            
        except Exception as e:
            raise EnhancedAnalysisError(
                f"Context-aware summarization failed: {str(e)}",
                "CONTEXT_SUMMARIZATION_ERROR",
                {"data_type": type(data).__name__, "error": str(e)},
                self.name,
                self.context
            )
    
    def _create_enhanced_summary(self, base_summary: Dict[str, Any], 
                               data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]:
        """Create enhanced summary with context integration."""
        enhanced_summary = base_summary.copy()  # Start with base summary
        
        # Add context-aware enhancements
        enhanced_summary['context_integration'] = {
            'analyzer_name': self.name,  # Analyzer identifier
            'analysis_timestamp': datetime.now().isoformat(),  # Analysis time
            'context_namespace': config.context_namespace,  # Context namespace
            'execution_id': f"summary_{int(time.time() * 1000)}",  # Execution ID
            'dependencies_checked': list(self.dependencies),  # Dependencies checked
            'shared_data_accessed': []  # Shared data accessed during analysis
        }
        
        # Add historical comparison if available
        if self.summary_history:  # Historical data available
            enhanced_summary['historical_comparison'] = self._compare_with_history(base_summary)
        
        # Add trend analysis
        enhanced_summary['trend_analysis'] = self._analyze_trends(base_summary)
        
        # Add context-based recommendations
        enhanced_summary['recommendations'] = self._generate_context_recommendations(base_summary, data)
        
        # Add performance metrics
        enhanced_summary['performance_metrics'] = self.analysis_metrics.copy()
        
        return enhanced_summary  # Return enhanced summary
    
    def _store_summary_in_context(self, summary: Dict[str, Any]) -> None:
        """Store summary results in context for future reference."""
        try:
            # Store current summary
            summary_key = f"{self.context_namespace}.{self.name}.latest_summary"
            self.context.set(summary_key, summary, f"{self.name}_summary")
            
            # Store in history
            history_key = f"{self.context_namespace}.{self.name}.summary_history"
            history = self.context.get(history_key) or []  # Get existing history
            
            # Add current summary to history (keep last 10)
            history.append({
                'timestamp': datetime.now().isoformat(),  # When summary was created
                'summary': summary,  # Summary data
                'execution_id': summary.get('context_integration', {}).get('execution_id')  # Execution ID
            })
            
            # Keep only recent history (last 10 summaries)
            if len(history) > 10:
                history = history[-10:]  # Keep last 10
            
            self.context.set(history_key, history, f"{self.name}_history")
            self.summary_history = history  # Update local history
            
            self.logger.debug(f"Stored summary in context with {len(history)} historical entries")
            
        except Exception as e:
            self.logger.warning(f"Failed to store summary in context: {str(e)}")
    
    def _compare_with_history(self, current_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Compare current summary with historical data."""
        comparison = {
            'has_history': True,  # Historical data available
            'history_count': len(self.summary_history),  # Number of historical summaries
            'trends': {},  # Trend information
            'changes': {}  # Changes from last summary
        }
        
        if not self.summary_history:  # No history available
            comparison['has_history'] = False
            return comparison
        
        try:
            # Get last summary for comparison
            last_summary = self.summary_history[-1]['summary']  # Most recent summary
            
            # Compare numeric statistics if available
            if 'numeric_analysis' in current_summary and 'numeric_analysis' in last_summary:
                current_numeric = current_summary['numeric_analysis']  # Current numeric data
                last_numeric = last_summary['numeric_analysis']  # Previous numeric data
                
                # Calculate changes in key metrics
                for metric in ['mean', 'median', 'std_dev', 'count']:
                    if metric in current_numeric and metric in last_numeric:
                        current_val = current_numeric[metric]  # Current value
                        last_val = last_numeric[metric]  # Previous value
                        
                        if last_val != 0:  # Avoid division by zero
                            change_percent = ((current_val - last_val) / last_val) * 100  # Calculate percentage change
                            comparison['changes'][metric] = {
                                'previous': last_val,  # Previous value
                                'current': current_val,  # Current value
                                'change_percent': change_percent,  # Percentage change
                                'trend': 'increasing' if change_percent > 0 else 'decreasing' if change_percent < 0 else 'stable'  # Trend direction
                            }
            
            # Calculate trend over multiple summaries
            if len(self.summary_history) >= 3:  # Need at least 3 data points
                comparison['trends'] = self._calculate_multi_period_trends()
            
        except Exception as e:
            self.logger.warning(f"Failed to compare with history: {str(e)}")
            comparison['error'] = str(e)  # Record error
        
        return comparison  # Return comparison results
    
    def _calculate_multi_period_trends(self) -> Dict[str, Any]:
        """Calculate trends across multiple historical periods."""
        trends = {}  # Initialize trends dictionary
        
        try:
            # Extract numeric values across history for trend calculation
            metrics_over_time = defaultdict(list)  # Store metrics over time
            
            for entry in self.summary_history[-5:]:  # Use last 5 entries
                summary = entry['summary']  # Get summary
                if 'numeric_analysis' in summary:  # Has numeric analysis
                    numeric_data = summary['numeric_analysis']  # Get numeric data
                    
                    for metric in ['mean', 'median', 'std_dev', 'count']:
                        if metric in numeric_data:
                            metrics_over_time[metric].append(numeric_data[metric])  # Add to time series
            
            # Calculate trends for each metric
            for metric, values in metrics_over_time.items():
                if len(values) >= 3:  # Need minimum data points
                    # Calculate linear trend
                    x_values = list(range(len(values)))  # X coordinates (time points)
                    
                    # Simple linear regression for trend detection
                    n = len(values)  # Number of points
                    sum_x = sum(x_values)  # Sum of x values
                    sum_y = sum(values)  # Sum of y values
                    sum_xy = sum(x * y for x, y in zip(x_values, values))  # Sum of x*y
                    sum_x2 = sum(x * x for x in x_values)  # Sum of x squared
                    
                    # Calculate slope (trend direction and magnitude)
                    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)  # Linear regression slope
                    
                    trends[metric] = {
                        'slope': slope,  # Trend slope
                        'direction': 'increasing' if slope > 0.1 else 'decreasing' if slope < -0.1 else 'stable',  # Trend direction
                        'strength': abs(slope),  # Trend strength (absolute slope)
                        'data_points': len(values),  # Number of data points used
                        'values': values  # Historical values
                    }
        
        except Exception as e:
            self.logger.warning(f"Failed to calculate multi-period trends: {str(e)}")
            trends['error'] = str(e)  # Record error
        
        return trends  # Return calculated trends
    
    def _analyze_trends(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current trends in the data."""
        trend_analysis = {
            'trend_detection_enabled': True,  # Trend detection is active
            'patterns_detected': [],  # List of detected patterns
            'statistical_trends': {},  # Statistical trend information
            'recommendations': []  # Trend-based recommendations
        }
        
        try:
            # Analyze numeric trends if available
            if 'numeric_analysis' in summary:  # Has numeric data
                numeric_data = summary['numeric_analysis']  # Get numeric analysis
                
                # Detect statistical anomalies
                if 'outliers' in numeric_data and numeric_data['outliers']['count'] > 0:
                    trend_analysis['patterns_detected'].append({
                        'type': 'outliers_detected',  # Pattern type
                        'count': numeric_data['outliers']['count'],  # Number of outliers
                        'percentage': numeric_data['outliers']['percentage'],  # Percentage of data
                        'significance': 'high' if numeric_data['outliers']['percentage'] > 10 else 'moderate'  # Significance level
                    })
                
                # Analyze distribution characteristics
                if 'std_dev' in numeric_data and 'mean' in numeric_data:
                    coefficient_of_variation = numeric_data['std_dev'] / numeric_data['mean'] if numeric_data['mean'] != 0 else 0  # Calculate CV
                    
                    trend_analysis['statistical_trends']['coefficient_of_variation'] = coefficient_of_variation
                    
                    if coefficient_of_variation > 1.0:  # High variability
                        trend_analysis['patterns_detected'].append({
                            'type': 'high_variability',  # Pattern type
                            'coefficient_of_variation': coefficient_of_variation,  # CV value
                            'interpretation': 'Data shows high variability relative to mean'  # Interpretation
                        })
                    elif coefficient_of_variation < 0.1:  # Low variability
                        trend_analysis['patterns_detected'].append({
                            'type': 'low_variability',  # Pattern type
                            'coefficient_of_variation': coefficient_of_variation,  # CV value
                            'interpretation': 'Data shows very consistent values'  # Interpretation
                        })
            
            # Generate trend-based recommendations
            if trend_analysis['patterns_detected']:  # Patterns were detected
                trend_analysis['recommendations'].extend(self._generate_trend_recommendations(trend_analysis['patterns_detected']))
        
        except Exception as e:
            self.logger.warning(f"Failed to analyze trends: {str(e)}")
            trend_analysis['error'] = str(e)  # Record error
        
        return trend_analysis  # Return trend analysis
    
    def _generate_context_recommendations(self, summary: Dict[str, Any], data: Any) -> List[str]:
        """Generate context-aware recommendations for data improvement."""
        recommendations = []  # Initialize recommendations list
        
        try:
            # Analyze data quality issues
            if 'quality_assessment' in summary:  # Quality assessment available
                quality = summary['quality_assessment']  # Get quality info
                
                if quality.get('overall_score', 1.0) < 0.7:  # Poor quality
                    recommendations.append("Consider data cleaning and validation to improve quality score")
                
                if 'issues' in quality and quality['issues']:  # Quality issues found
                    recommendations.append(f"Address data quality issues: {', '.join(quality['issues'])}")
            
            # Analyze missing values
            if 'missing_values' in summary:  # Missing value info available
                missing = summary['missing_values']  # Get missing value data
                
                if missing.get('missing_percentage', 0) > 20:  # High missing percentage
                    recommendations.append("High percentage of missing values detected - consider imputation or data collection strategies")
            
            # Analyze statistical characteristics
            if 'numeric_analysis' in summary:  # Numeric analysis available
                numeric = summary['numeric_analysis']  # Get numeric data
                
                if 'outliers' in numeric and numeric['outliers']['percentage'] > 15:  # Many outliers
                    recommendations.append("High number of outliers detected - consider outlier treatment or data validation")
                
                if 'std_dev' in numeric and 'mean' in numeric:
                    cv = numeric['std_dev'] / numeric['mean'] if numeric['mean'] != 0 else 0  # Coefficient of variation
                    
                    if cv > 2.0:  # Very high variability
                        recommendations.append("Extremely high data variability - consider segmentation or different analysis approaches")
            
            # Context-specific recommendations
            if hasattr(self, 'context') and self.context:  # Context available
                try:
                    # Check if this is part of a pipeline
                    pipeline_info = self.context.get(f"{self.context_namespace}.pipeline.current")
                    if pipeline_info:  # Part of pipeline
                        recommendations.append("Consider data consistency with other pipeline components")
                    
                    # Check for shared data availability
                    shared_data_keys = [key for key in self.context.get_all_keys() if f"{self.context_namespace}.shared_data" in key]
                    if shared_data_keys:  # Shared data available
                        recommendations.append("Leverage shared data from other analyzers for enhanced insights")
                
                except Exception:
                    pass  # Ignore context access errors
            
            # Default recommendation if no specific issues
            if not recommendations:
                recommendations.append("Data quality appears good - consider advanced analytics for deeper insights")
        
        except Exception as e:
            self.logger.warning(f"Failed to generate context recommendations: {str(e)}")
            recommendations.append("Unable to generate context-specific recommendations due to analysis error")
        
        return recommendations  # Return generated recommendations
    
    def _generate_trend_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on detected patterns."""
        recommendations = []  # Initialize recommendations
        
        for pattern in patterns:  # Check each detected pattern
            pattern_type = pattern.get('type')  # Get pattern type
            
            if pattern_type == 'outliers_detected':  # Outliers found
                if pattern.get('significance') == 'high':  # High significance outliers
                    recommendations.append("Investigate high-significance outliers for data quality or interesting phenomena")
                else:
                    recommendations.append("Monitor outliers for potential data quality issues")
            
            elif pattern_type == 'high_variability':  # High variability detected
                recommendations.append("Consider data segmentation or stratified analysis due to high variability")
            
            elif pattern_type == 'low_variability':  # Low variability detected
                recommendations.append("Data shows consistency - suitable for precise statistical analysis")
        
        return recommendations  # Return pattern-based recommendations
    
    def _update_performance_metrics(self, start_time: float, data_size: int) -> None:
        """Update performance tracking metrics."""
        try:
            execution_time = time.time() - start_time  # Calculate execution time
            
            # Update metrics
            self.analysis_metrics['total_analyses'] += 1  # Increment analysis count
            self.analysis_metrics['total_data_points'] += data_size  # Add data points processed
            
            # Update average processing time
            current_avg = self.analysis_metrics['average_processing_time']  # Current average
            total_analyses = self.analysis_metrics['total_analyses']  # Total analyses
            self.analysis_metrics['average_processing_time'] = ((current_avg * (total_analyses - 1)) + execution_time) / total_analyses  # New average
            
            # Store metrics in context if available
            if hasattr(self, 'context') and self.context:  # Context available
                metrics_key = f"{self.context_namespace}.{self.name}.performance_metrics"
                self.context.set(metrics_key, self.analysis_metrics, f"{self.name}_metrics")
        
        except Exception as e:
            self.logger.warning(f"Failed to update performance metrics: {str(e)}")
    
    def _track_analysis_trends(self, summary: Dict[str, Any]) -> None:
        """Track analysis trends for long-term monitoring."""
        try:
            # Extract key metrics for trending
            if 'numeric_analysis' in summary:  # Numeric data available
                numeric = summary['numeric_analysis']  # Get numeric analysis
                
                # Track key metrics over time
                for metric in ['mean', 'median', 'std_dev', 'count']:
                    if metric in numeric:  # Metric available
                        self.trend_tracking[metric].append(numeric[metric])  # Add to trend data
                        
                        # Keep only recent trends (last 50 data points)
                        if len(self.trend_tracking[metric]) > 50:
                            self.trend_tracking[metric] = self.trend_tracking[metric][-50:]  # Keep recent data
            
            # Store trends in context
            if hasattr(self, 'context') and self.context:  # Context available
                trends_key = f"{self.context_namespace}.{self.name}.trend_tracking"
                # Convert defaultdict to regular dict for JSON serialization
                trends_dict = {k: v for k, v in self.trend_tracking.items()}
                self.context.set(trends_key, trends_dict, f"{self.name}_trends")
        
        except Exception as e:
            self.logger.warning(f"Failed to track analysis trends: {str(e)}")


class MetricsAnalyzer(EnhancedAnalyzerV2):
    """
    Comprehensive metrics analyzer with Context integration.
    
    Provides advanced metrics collection, analysis, and monitoring
    capabilities with full Context system integration.
    
    Features:
        - Real-time performance monitoring
        - Resource usage tracking
        - Context-aware metric correlation
        - Historical trend analysis
        - Alert generation and notification
    """
    
    def __init__(self, name: str = "metrics_analyzer",
                 config: Optional[EnhancedAnalysisConfig] = None,
                 context: Optional[Context] = None) -> None:
        """Initialize metrics analyzer with enhanced capabilities."""
        super().__init__(name, config, context)  # Initialize enhanced analyzer
        
        # Metrics tracking
        self.metrics_store: Dict[str, List[Dict[str, Any]]] = defaultdict(list)  # Metrics storage
        self.alert_thresholds: Dict[str, Dict[str, float]] = {}  # Alert thresholds
        self.active_alerts: List[Dict[str, Any]] = []  # Active alert list
        
        self.logger.info(f"MetricsAnalyzer '{name}' initialized with Context integration")
    
    def _analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Dict[str, Any]:
        """
        Perform comprehensive metrics analysis.
        
        Args:
            data: Metrics data for analysis (can be various formats)
            config: Enhanced analysis configuration
            
        Returns:
            Dictionary containing comprehensive metrics analysis
        """
        metrics_result = {
            'analysis_type': 'comprehensive_metrics',  # Analysis type identifier
            'timestamp': datetime.now().isoformat(),  # Analysis timestamp
            'metrics_collected': {},  # Collected metrics
            'performance_analysis': {},  # Performance analysis results
            'trend_analysis': {},  # Trend analysis results
            'alerts': [],  # Generated alerts
            'recommendations': []  # Analysis recommendations
        }
        
        try:
            # Collect and analyze metrics
            metrics_result['metrics_collected'] = self._collect_metrics(data)  # Collect metrics
            
            # Perform performance analysis
            metrics_result['performance_analysis'] = self._analyze_performance_metrics(metrics_result['metrics_collected'])
            
            # Analyze trends
            metrics_result['trend_analysis'] = self._analyze_metric_trends()
            
            # Check for alerts
            metrics_result['alerts'] = self._check_alert_conditions(metrics_result['metrics_collected'])
            
            # Generate recommendations
            metrics_result['recommendations'] = self._generate_metrics_recommendations(metrics_result)
            
            # Store results in context
            if config.enable_context_integration:
                self._store_metrics_in_context(metrics_result)
            
            return metrics_result  # Return metrics analysis
            
        except Exception as e:
            raise EnhancedAnalysisError(
                f"Metrics analysis failed: {str(e)}",
                "METRICS_ANALYSIS_ERROR",
                {"error": str(e)},
                self.name,
                self.context
            )
    
    def _collect_metrics(self, data: Any) -> Dict[str, Any]:
        """Collect comprehensive metrics from input data."""
        collected_metrics = {
            'collection_timestamp': datetime.now().isoformat(),  # When metrics were collected
            'data_metrics': {},  # Metrics about the data itself
            'context_metrics': {},  # Metrics from context system
            'system_metrics': {}  # System-level metrics
        }
        
        # Analyze input data metrics
        if isinstance(data, dict):  # Dictionary data
            collected_metrics['data_metrics'] = self._analyze_dict_metrics(data)
        elif isinstance(data, (list, tuple)):  # Sequence data
            collected_metrics['data_metrics'] = self._analyze_sequence_metrics(data)
        else:  # Other data types
            collected_metrics['data_metrics'] = self._analyze_general_metrics(data)
        
        # Collect context system metrics if available
        if hasattr(self, 'context') and self.context:
            collected_metrics['context_metrics'] = self._collect_context_metrics()
        
        return collected_metrics  # Return collected metrics
    
    def _analyze_dict_metrics(self, data: Dict) -> Dict[str, Any]:
        """Analyze metrics for dictionary data."""
        return {
            'key_count': len(data),  # Number of keys
            'value_types': Counter(type(v).__name__ for v in data.values()),  # Value type distribution
            'null_values': sum(1 for v in data.values() if v is None),  # Count of null values
            'nested_structures': sum(1 for v in data.values() if isinstance(v, (dict, list))),  # Nested structure count
            'memory_estimate_bytes': len(str(data))  # Rough memory estimate
        }
    
    def _analyze_sequence_metrics(self, data: Union[List, Tuple]) -> Dict[str, Any]:
        """Analyze metrics for sequence data."""
        numeric_data = [x for x in data if isinstance(x, (int, float))]  # Extract numeric values
        
        metrics = {
            'length': len(data),  # Sequence length
            'element_types': Counter(type(x).__name__ for x in data),  # Element type distribution
            'null_count': sum(1 for x in data if x is None),  # Null element count
            'memory_estimate_bytes': len(str(data))  # Rough memory estimate
        }
        
        if numeric_data:  # Add numeric metrics if available
            metrics['numeric_metrics'] = {
                'count': len(numeric_data),  # Count of numeric values
                'mean': statistics.mean(numeric_data),  # Average value
                'median': statistics.median(numeric_data),  # Median value
                'std_dev': statistics.stdev(numeric_data) if len(numeric_data) > 1 else 0,  # Standard deviation
                'min': min(numeric_data),  # Minimum value
                'max': max(numeric_data),  # Maximum value
                'sum': sum(numeric_data)  # Sum of values
            }
        
        return metrics  # Return sequence metrics
    
    def _analyze_general_metrics(self, data: Any) -> Dict[str, Any]:
        """Analyze metrics for general data types."""
        return {
            'data_type': type(data).__name__,  # Data type name
            'string_length': len(str(data)),  # String representation length
            'is_none': data is None,  # Whether data is None
            'is_callable': callable(data),  # Whether data is callable
            'memory_estimate_bytes': len(str(data))  # Rough memory estimate
        }
    
    def _collect_context_metrics(self) -> Dict[str, Any]:
        """Collect metrics from the Context system."""
        context_metrics = {}  # Initialize context metrics
        
        try:
            # Get basic context information
            all_keys = self.context.keys()  # Get all context keys
            context_metrics['total_keys'] = len(all_keys)  # Total number of keys
            
            # Analyze key namespaces
            namespace_counts = defaultdict(int)  # Count keys by namespace
            for key in all_keys:
                namespace = key.split('.')[0] if '.' in key else 'root'  # Extract namespace
                namespace_counts[namespace] += 1  # Increment count
            
            context_metrics['namespace_distribution'] = dict(namespace_counts)  # Store distribution
            
            # Analyzer-specific metrics
            analyzer_keys = [key for key in all_keys if f"{self.context_namespace}.{self.name}" in key]
            context_metrics['analyzer_keys_count'] = len(analyzer_keys)  # Keys for this analyzer
            
            # Context usage metrics
            if hasattr(self.context, 'get_metrics') and callable(self.context.get_metrics):
                try:
                    context_system_metrics = self.context.get_metrics()  # Get context system metrics
                    context_metrics['context_system_metrics'] = context_system_metrics
                except Exception:
                    pass  # Ignore if metrics not available
        
        except Exception as e:
            self.logger.warning(f"Failed to collect context metrics: {str(e)}")
            context_metrics['error'] = str(e)  # Record error
        
        return context_metrics  # Return context metrics
    
    def _analyze_performance_metrics(self, collected_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance characteristics of collected metrics."""
        performance_analysis = {
            'analysis_timestamp': datetime.now().isoformat(),  # Analysis timestamp
            'performance_indicators': {},  # Performance indicators
            'bottleneck_analysis': {},  # Bottleneck identification
            'efficiency_metrics': {}  # Efficiency measurements
        }
        
        try:
            # Analyze data processing efficiency
            data_metrics = collected_metrics.get('data_metrics', {})  # Get data metrics
            
            if 'memory_estimate_bytes' in data_metrics:
                memory_mb = data_metrics['memory_estimate_bytes'] / (1024 * 1024)  # Convert to MB
                performance_analysis['performance_indicators']['memory_usage_mb'] = memory_mb
                
                if memory_mb > 100:  # High memory usage
                    performance_analysis['bottleneck_analysis']['high_memory_usage'] = {
                        'detected': True,  # High usage detected
                        'value_mb': memory_mb,  # Memory usage in MB
                        'recommendation': 'Consider data chunking or streaming for large datasets'
                    }
            
            # Analyze context system performance
            context_metrics = collected_metrics.get('context_metrics', {})  # Get context metrics
            
            if 'total_keys' in context_metrics:
                total_keys = context_metrics['total_keys']  # Total context keys
                performance_analysis['performance_indicators']['context_key_count'] = total_keys
                
                if total_keys > 1000:  # Many context keys
                    performance_analysis['bottleneck_analysis']['high_context_usage'] = {
                        'detected': True,  # High usage detected
                        'key_count': total_keys,  # Number of keys
                        'recommendation': 'Consider context key cleanup or namespacing optimization'
                    }
        
        except Exception as e:
            self.logger.warning(f"Failed to analyze performance metrics: {str(e)}")
            performance_analysis['error'] = str(e)  # Record error
        
        return performance_analysis  # Return performance analysis
    
    def _analyze_metric_trends(self) -> Dict[str, Any]:
        """Analyze trends in collected metrics over time."""
        trend_analysis = {
            'trend_analysis_timestamp': datetime.now().isoformat(),  # Analysis timestamp
            'metric_trends': {},  # Individual metric trends
            'correlation_analysis': {},  # Metric correlations
            'trend_summary': {}  # Overall trend summary
        }
        
        try:
            # Analyze trends for each stored metric
            for metric_name, metric_history in self.metrics_store.items():
                if len(metric_history) >= 3:  # Need minimum data points
                    trend_analysis['metric_trends'][metric_name] = self._calculate_metric_trend(metric_history)
            
            # Calculate overall trends
            if trend_analysis['metric_trends']:
                trend_analysis['trend_summary'] = self._summarize_metric_trends(trend_analysis['metric_trends'])
        
        except Exception as e:
            self.logger.warning(f"Failed to analyze metric trends: {str(e)}")
            trend_analysis['error'] = str(e)  # Record error
        
        return trend_analysis  # Return trend analysis
    
    def _calculate_metric_trend(self, metric_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate trend for a specific metric."""
        trend_info = {
            'data_points': len(metric_history),  # Number of data points
            'time_span_minutes': 0,  # Time span of data
            'trend_direction': 'stable',  # Trend direction
            'trend_strength': 0.0,  # Trend strength
            'latest_value': None,  # Most recent value
            'change_from_first': 0.0  # Change from first to last
        }
        
        try:
            if len(metric_history) < 2:  # Insufficient data
                return trend_info
            
            # Extract timestamps and values
            timestamps = []  # List of timestamps
            values = []  # List of values
            
            for entry in metric_history:
                if 'timestamp' in entry and 'value' in entry:
                    timestamps.append(datetime.fromisoformat(entry['timestamp']))  # Convert timestamp
                    values.append(entry['value'])  # Extract value
            
            if len(values) < 2:  # Insufficient numeric values
                return trend_info
            
            # Calculate time span
            if timestamps:
                time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 60  # Minutes
                trend_info['time_span_minutes'] = time_span
            
            # Calculate trend direction and strength
            first_value = values[0]  # First value
            last_value = values[-1]  # Last value
            trend_info['latest_value'] = last_value
            
            if first_value != 0:  # Avoid division by zero
                change_percent = ((last_value - first_value) / first_value) * 100  # Percentage change
                trend_info['change_from_first'] = change_percent
                
                if change_percent > 5:  # Increasing trend
                    trend_info['trend_direction'] = 'increasing'
                    trend_info['trend_strength'] = abs(change_percent)
                elif change_percent < -5:  # Decreasing trend
                    trend_info['trend_direction'] = 'decreasing'
                    trend_info['trend_strength'] = abs(change_percent)
                else:  # Stable trend
                    trend_info['trend_direction'] = 'stable'
                    trend_info['trend_strength'] = abs(change_percent)
        
        except Exception as e:
            trend_info['error'] = str(e)  # Record error
        
        return trend_info  # Return trend information
    
    def _summarize_metric_trends(self, metric_trends: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize overall trends across all metrics."""
        summary = {
            'total_metrics': len(metric_trends),  # Total number of metrics
            'trending_up': 0,  # Count of increasing trends
            'trending_down': 0,  # Count of decreasing trends
            'stable': 0,  # Count of stable trends
            'strongest_trends': [],  # List of strongest trends
            'overall_assessment': 'mixed'  # Overall trend assessment
        }
        
        # Count trend directions
        for metric_name, trend_info in metric_trends.items():
            direction = trend_info.get('trend_direction', 'stable')  # Get trend direction
            
            if direction == 'increasing':
                summary['trending_up'] += 1
            elif direction == 'decreasing':
                summary['trending_down'] += 1
            else:
                summary['stable'] += 1
            
            # Track strongest trends
            strength = trend_info.get('trend_strength', 0)  # Get trend strength
            if strength > 10:  # Strong trend
                summary['strongest_trends'].append({
                    'metric': metric_name,  # Metric name
                    'direction': direction,  # Trend direction
                    'strength': strength  # Trend strength
                })
        
        # Determine overall assessment
        if summary['trending_up'] > summary['trending_down'] * 2:
            summary['overall_assessment'] = 'predominantly_increasing'
        elif summary['trending_down'] > summary['trending_up'] * 2:
            summary['overall_assessment'] = 'predominantly_decreasing'
        elif summary['stable'] > (summary['trending_up'] + summary['trending_down']):
            summary['overall_assessment'] = 'mostly_stable'
        else:
            summary['overall_assessment'] = 'mixed'
        
        return summary  # Return trend summary
    
    def _check_alert_conditions(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check collected metrics against alert thresholds."""
        alerts = []  # Initialize alerts list
        
        try:
            # Check data metrics alerts
            data_metrics = metrics.get('data_metrics', {})  # Get data metrics
            
            # Memory usage alert
            if 'memory_estimate_bytes' in data_metrics:
                memory_mb = data_metrics['memory_estimate_bytes'] / (1024 * 1024)  # Convert to MB
                
                if memory_mb > 500:  # High memory usage threshold
                    alerts.append({
                        'type': 'high_memory_usage',  # Alert type
                        'severity': 'warning',  # Alert severity
                        'metric': 'memory_usage_mb',  # Metric name
                        'value': memory_mb,  # Metric value
                        'threshold': 500,  # Alert threshold
                        'message': f'High memory usage detected: {memory_mb:.2f} MB',  # Alert message
                        'timestamp': datetime.now().isoformat()  # Alert timestamp
                    })
            
            # Context key count alert
            context_metrics = metrics.get('context_metrics', {})  # Get context metrics
            if 'total_keys' in context_metrics:
                key_count = context_metrics['total_keys']  # Get key count
                
                if key_count > 2000:  # High key count threshold
                    alerts.append({
                        'type': 'high_context_key_count',  # Alert type
                        'severity': 'warning',  # Alert severity
                        'metric': 'context_key_count',  # Metric name
                        'value': key_count,  # Metric value
                        'threshold': 2000,  # Alert threshold
                        'message': f'High context key count detected: {key_count} keys',  # Alert message
                        'timestamp': datetime.now().isoformat()  # Alert timestamp
                    })
        
        except Exception as e:
            self.logger.warning(f"Failed to check alert conditions: {str(e)}")
        
        return alerts  # Return generated alerts
    
    def _generate_metrics_recommendations(self, metrics_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on metrics analysis."""
        recommendations = []  # Initialize recommendations list
        
        try:
            # Performance-based recommendations
            performance = metrics_result.get('performance_analysis', {})  # Get performance analysis
            
            if 'bottleneck_analysis' in performance:  # Bottlenecks detected
                for bottleneck_type, info in performance['bottleneck_analysis'].items():
                    if info.get('detected'):  # Bottleneck detected
                        recommendations.append(info.get('recommendation', f'Address {bottleneck_type}'))
            
            # Alert-based recommendations
            alerts = metrics_result.get('alerts', [])  # Get alerts
            if alerts:
                recommendations.append(f"Address {len(alerts)} active alert(s) to improve system performance")
            
            # Trend-based recommendations
            trends = metrics_result.get('trend_analysis', {}).get('trend_summary', {})  # Get trend summary
            
            if trends.get('overall_assessment') == 'predominantly_decreasing':
                recommendations.append("Monitor decreasing trends - may indicate performance degradation")
            elif trends.get('overall_assessment') == 'predominantly_increasing':
                recommendations.append("Monitor increasing trends - may indicate resource growth or load increase")
            
            # Default recommendations
            if not recommendations:
                recommendations.append("Metrics appear normal - continue regular monitoring")
        
        except Exception as e:
            self.logger.warning(f"Failed to generate metrics recommendations: {str(e)}")
            recommendations.append("Unable to generate recommendations due to analysis error")
        
        return recommendations  # Return generated recommendations
    
    def _store_metrics_in_context(self, metrics_result: Dict[str, Any]) -> None:
        """Store metrics analysis results in context."""
        try:
            # Store latest metrics
            latest_key = f"{self.context_namespace}.{self.name}.latest_metrics"
            self.context.set(latest_key, metrics_result, f"{self.name}_metrics")
            
            # Add to metrics history
            timestamp = datetime.now().isoformat()  # Current timestamp
            history_entry = {
                'timestamp': timestamp,  # Entry timestamp
                'metrics': metrics_result,  # Metrics data
                'execution_id': f"metrics_{int(time.time() * 1000)}"  # Execution ID
            }
            
            # Store individual metrics for trending
            if 'metrics_collected' in metrics_result:  # Metrics available
                collected = metrics_result['metrics_collected']  # Get collected metrics
                
                # Store data metrics
                if 'data_metrics' in collected:
                    for metric_name, value in collected['data_metrics'].items():
                        if isinstance(value, (int, float)):  # Numeric metric
                            self.metrics_store[metric_name].append({
                                'timestamp': timestamp,  # Metric timestamp
                                'value': value  # Metric value
                            })
                            
                            # Keep only recent history
                            if len(self.metrics_store[metric_name]) > 100:
                                self.metrics_store[metric_name] = self.metrics_store[metric_name][-100:]
            
            self.logger.debug(f"Stored metrics analysis in context")
        
        except Exception as e:
            self.logger.warning(f"Failed to store metrics in context: {str(e)}")


# Register enhanced components
from .registry import register_analyzer

@register_analyzer(
    name="context_aware_summarizer",
    description="Context-aware data summarizer with enhanced tracking",
    version="2.0.0",
    dependencies=["orchestrator.context"]
)
class RegisteredContextAwareSummarizer(ContextAwareSummarizer):
    """Registered version of ContextAwareSummarizer for automatic discovery."""
    pass


@register_analyzer(
    name="metrics_analyzer", 
    description="Comprehensive metrics analyzer with Context integration",
    version="2.0.0",
    dependencies=["orchestrator.context"]
)
class RegisteredMetricsAnalyzer(MetricsAnalyzer):
    """Registered version of MetricsAnalyzer for automatic discovery."""
    pass


# Export enhanced components
__all__ = [
    'ContextAwareSummarizer',
    'MetricsAnalyzer',
    'RegisteredContextAwareSummarizer',
    'RegisteredMetricsAnalyzer'
]