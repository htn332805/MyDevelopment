"""
Enhanced Analysis Framework with Context Integration

This module provides the enhanced analysis framework that integrates with the
consolidated Context system, providing comprehensive traceability, metrics,
and advanced features for Framework0.

Features:
    - Full Context system integration for traceability
    - Advanced dependency tracking and resolution  
    - Plugin architecture with dynamic loading
    - Enhanced performance monitoring and optimization
    - Comprehensive error handling and recovery
    - Cross-analyzer communication and data sharing
    - Memory management and resource optimization
    - Real-time analysis pipeline execution
"""

import os
import time
import json
import threading
import traceback
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, Generic, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

# Import core systems
from src.core.logger import get_logger
from orchestrator.context.context import Context

# Import existing framework components
try:
    from .framework import BaseAnalyzerV2, AnalysisConfig, AnalysisResult, AnalysisError
except ImportError:
    from src.analysis.framework import BaseAnalyzerV2, AnalysisConfig, AnalysisResult, AnalysisError
from .registry import AnalysisRegistry

# Type variable for generic result types
T = TypeVar('T')

class EnhancedAnalysisError(AnalysisError):
    """
    Enhanced analysis error with Context integration and advanced error tracking.
    
    Provides comprehensive error information including context state,
    execution trace, and recovery suggestions.
    """
    
    def __init__(self, message: str, error_code: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None,
                 analyzer_name: Optional[str] = None,
                 execution_context: Optional[Context] = None) -> None:
        """Initialize enhanced error with Context integration."""
        super().__init__(message, error_code, context)  # Call parent constructor
        self.analyzer_name = analyzer_name or "unknown"  # Analyzer that caused error
        self.execution_trace = traceback.format_stack()  # Capture execution stack
        self.context_state = None  # Context state at error time
        
        # Capture context state if available
        if execution_context:  # Context available
            try:
                self.context_state = execution_context.keys()  # Get context snapshot
            except Exception:
                self.context_state = {"error": "Failed to capture context state"}  # Error capturing state


@dataclass
class EnhancedAnalysisConfig(AnalysisConfig):
    """
    Enhanced analysis configuration with Context integration and advanced features.
    
    Extends base configuration with Context system integration,
    pipeline management, and advanced optimization settings.
    """
    
    # Context integration settings
    enable_context_integration: bool = True  # Whether to use Context system
    context_namespace: str = "analysis"  # Namespace for context keys
    track_execution_metrics: bool = True  # Whether to track detailed metrics
    
    # Pipeline settings
    enable_pipeline_mode: bool = False  # Whether operating in pipeline mode
    pipeline_name: str = "default"  # Name for pipeline execution
    enable_inter_analyzer_communication: bool = True  # Whether analyzers can communicate
    
    # Performance settings
    enable_memory_optimization: bool = True  # Whether to optimize memory usage
    enable_result_caching: bool = True  # Whether to cache analysis results
    cache_expiry_seconds: int = 3600  # Cache expiry time in seconds
    
    # Monitoring settings
    enable_performance_monitoring: bool = True  # Whether to monitor performance
    enable_resource_tracking: bool = True  # Whether to track resource usage
    alert_on_resource_limits: bool = True  # Whether to alert on resource limits
    
    # Error handling settings
    enable_error_recovery: bool = True  # Whether to attempt error recovery
    max_retry_attempts: int = 3  # Maximum retry attempts on failure
    retry_delay_seconds: float = 1.0  # Delay between retry attempts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert enhanced configuration to dictionary."""
        base_dict = super().to_dict()  # Get base configuration dictionary
        
        # Add enhanced settings
        base_dict.update({
            'enable_context_integration': self.enable_context_integration,  # Context integration flag
            'context_namespace': self.context_namespace,  # Context namespace
            'track_execution_metrics': self.track_execution_metrics,  # Metrics tracking flag
            'enable_pipeline_mode': self.enable_pipeline_mode,  # Pipeline mode flag
            'pipeline_name': self.pipeline_name,  # Pipeline name
            'enable_inter_analyzer_communication': self.enable_inter_analyzer_communication,  # Communication flag
            'enable_memory_optimization': self.enable_memory_optimization,  # Memory optimization flag
            'enable_result_caching': self.enable_result_caching,  # Caching flag
            'cache_expiry_seconds': self.cache_expiry_seconds,  # Cache expiry time
            'enable_performance_monitoring': self.enable_performance_monitoring,  # Performance monitoring flag
            'enable_resource_tracking': self.enable_resource_tracking,  # Resource tracking flag
            'alert_on_resource_limits': self.alert_on_resource_limits,  # Resource alert flag
            'enable_error_recovery': self.enable_error_recovery,  # Error recovery flag
            'max_retry_attempts': self.max_retry_attempts,  # Maximum retries
            'retry_delay_seconds': self.retry_delay_seconds  # Retry delay
        })
        
        return base_dict  # Return complete dictionary
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'EnhancedAnalysisConfig':
        """Create enhanced configuration from dictionary."""
        # Get valid keys for enhanced config
        valid_keys = {
            # Base config keys
            'timeout_seconds', 'enable_threading', 'max_memory_mb', 'debug_mode',
            'statistical_precision', 'pattern_threshold', 'quality_threshold',
            'include_raw_data', 'format_output', 'save_intermediate',
            'pre_analysis_hooks', 'post_analysis_hooks',
            # Enhanced config keys
            'enable_context_integration', 'context_namespace', 'track_execution_metrics',
            'enable_pipeline_mode', 'pipeline_name', 'enable_inter_analyzer_communication',
            'enable_memory_optimization', 'enable_result_caching', 'cache_expiry_seconds',
            'enable_performance_monitoring', 'enable_resource_tracking', 'alert_on_resource_limits',
            'enable_error_recovery', 'max_retry_attempts', 'retry_delay_seconds'
        }
        
        # Filter valid keys
        filtered_dict = {k: v for k, v in config_dict.items() if k in valid_keys}
        
        return cls(**filtered_dict)  # Create enhanced config instance


@dataclass
class EnhancedAnalysisResult(AnalysisResult[T]):
    """
    Enhanced analysis result with Context integration and advanced metadata.
    
    Extends base result with Context system integration, dependency tracking,
    and comprehensive execution information.
    """
    
    # Context integration information
    context_namespace: str = "analysis"  # Context namespace used
    context_keys_created: List[str] = field(default_factory=list)  # Keys created in context
    context_keys_accessed: List[str] = field(default_factory=list)  # Keys accessed from context
    
    # Execution tracking
    execution_id: str = field(default_factory=lambda: f"exec_{int(time.time() * 1000)}")  # Unique execution ID
    pipeline_id: Optional[str] = None  # Pipeline ID if part of pipeline
    parent_execution_id: Optional[str] = None  # Parent execution for nested analysis
    
    # Performance metrics
    cpu_time: float = 0.0  # CPU time used in seconds
    peak_memory_mb: float = 0.0  # Peak memory usage in megabytes
    io_operations: int = 0  # Number of I/O operations
    cache_hits: int = 0  # Number of cache hits
    cache_misses: int = 0  # Number of cache misses
    
    # Dependency information
    dependencies_resolved: List[str] = field(default_factory=list)  # Resolved dependencies
    dependencies_failed: List[str] = field(default_factory=list)  # Failed dependencies
    dependent_analyzers: List[str] = field(default_factory=list)  # Analyzers depending on this result
    
    # Communication tracking
    messages_sent: int = 0  # Messages sent to other analyzers
    messages_received: int = 0  # Messages received from other analyzers
    data_shared: List[str] = field(default_factory=list)  # Data keys shared with other analyzers
    
    def add_context_key_created(self, key: str) -> None:
        """Record that a context key was created."""
        if key not in self.context_keys_created:  # Avoid duplicates
            self.context_keys_created.append(key)  # Add to created keys
    
    def add_context_key_accessed(self, key: str) -> None:
        """Record that a context key was accessed."""
        if key not in self.context_keys_accessed:  # Avoid duplicates
            self.context_keys_accessed.append(key)  # Add to accessed keys
    
    def add_dependency_resolved(self, dependency: str) -> None:
        """Record that a dependency was resolved."""
        if dependency not in self.dependencies_resolved:  # Avoid duplicates
            self.dependencies_resolved.append(dependency)  # Add to resolved dependencies
    
    def add_dependency_failed(self, dependency: str) -> None:
        """Record that a dependency failed to resolve."""
        if dependency not in self.dependencies_failed:  # Avoid duplicates
            self.dependencies_failed.append(dependency)  # Add to failed dependencies
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert enhanced result to dictionary."""
        base_dict = super().to_dict()  # Get base result dictionary
        
        # Add enhanced metadata
        base_dict.update({
            'context_namespace': self.context_namespace,  # Context namespace
            'context_keys_created': self.context_keys_created.copy(),  # Created context keys
            'context_keys_accessed': self.context_keys_accessed.copy(),  # Accessed context keys
            'execution_id': self.execution_id,  # Execution ID
            'pipeline_id': self.pipeline_id,  # Pipeline ID
            'parent_execution_id': self.parent_execution_id,  # Parent execution ID
            'cpu_time': self.cpu_time,  # CPU time used
            'peak_memory_mb': self.peak_memory_mb,  # Peak memory usage
            'io_operations': self.io_operations,  # I/O operations count
            'cache_hits': self.cache_hits,  # Cache hits count
            'cache_misses': self.cache_misses,  # Cache misses count
            'dependencies_resolved': self.dependencies_resolved.copy(),  # Resolved dependencies
            'dependencies_failed': self.dependencies_failed.copy(),  # Failed dependencies
            'dependent_analyzers': self.dependent_analyzers.copy(),  # Dependent analyzers
            'messages_sent': self.messages_sent,  # Messages sent count
            'messages_received': self.messages_received,  # Messages received count
            'data_shared': self.data_shared.copy()  # Shared data keys
        })
        
        return base_dict  # Return enhanced dictionary


class EnhancedAnalyzerV2(BaseAnalyzerV2):
    """
    Enhanced analyzer base class with Context integration and advanced features.
    
    Extends BaseAnalyzerV2 with Context system integration, dependency management,
    advanced error handling, and inter-analyzer communication capabilities.
    
    Features:
        - Full Context system integration for state management
        - Advanced dependency tracking and resolution
        - Inter-analyzer communication and data sharing
        - Enhanced error handling with recovery mechanisms  
        - Performance monitoring and resource optimization
        - Plugin architecture support
        - Real-time pipeline execution
    """
    
    def __init__(self, name: str, config: Optional[EnhancedAnalysisConfig] = None,
                 context: Optional[Context] = None) -> None:
        """
        Initialize enhanced analyzer with Context integration.
        
        Args:
            name: Unique analyzer name
            config: Enhanced configuration (uses defaults if None)
            context: Context instance for state management (creates if None)
        """
        # Initialize base analyzer with enhanced config
        enhanced_config = config or EnhancedAnalysisConfig()
        super().__init__(name, enhanced_config)  # Call parent constructor
        
        # Context system integration
        self.context = context or Context(enable_history=True, enable_metrics=True)  # Initialize context
        self.context_namespace = enhanced_config.context_namespace  # Store context namespace
        
        # Enhanced tracking
        self.dependencies: Set[str] = set()  # Set of analyzer dependencies
        self.dependents: Set[str] = set()  # Set of dependent analyzers
        self.communication_channels: Dict[str, List[Any]] = {}  # Inter-analyzer communication
        
        # Performance tracking
        self.execution_history: List[Dict[str, Any]] = []  # Execution history
        self.resource_usage: Dict[str, float] = {}  # Resource usage tracking
        self.cache: Dict[str, Tuple[Any, float]] = {}  # Result cache with timestamps
        
        # Error handling
        self.retry_count = 0  # Current retry attempt count
        self.last_error: Optional[EnhancedAnalysisError] = None  # Last error encountered
        
        # Initialize context keys
        if enhanced_config.enable_context_integration:  # Context integration enabled
            self._initialize_context_keys()  # Set up context keys
        
        self.logger.info(f"Enhanced analyzer '{name}' initialized with Context integration")
    
    def _initialize_context_keys(self) -> None:
        """Initialize analyzer-specific context keys."""
        try:
            # Set analyzer metadata in context
            self.context.set(f"{self.context_namespace}.{self.name}.initialized", True, f"{self.name}_init")
            self.context.set(f"{self.context_namespace}.{self.name}.config", self.config.to_dict(), f"{self.name}_init")
            self.context.set(f"{self.context_namespace}.{self.name}.created_at", datetime.now().isoformat(), f"{self.name}_init")
            
            self.logger.debug(f"Initialized context keys for analyzer '{self.name}'")
        except Exception as e:
            self.logger.warning(f"Failed to initialize context keys: {str(e)}")
    
    def add_dependency(self, analyzer_name: str) -> None:
        """Add analyzer dependency."""
        self.dependencies.add(analyzer_name)  # Add to dependencies
        
        # Update context with dependency information
        if isinstance(self.config, EnhancedAnalysisConfig) and self.config.enable_context_integration:
            try:
                deps_list = list(self.dependencies)  # Convert to list
                self.context.set(f"{self.context_namespace}.{self.name}.dependencies", deps_list, f"{self.name}_deps")
                self.logger.debug(f"Added dependency '{analyzer_name}' to analyzer '{self.name}'")
            except Exception as e:
                self.logger.warning(f"Failed to update context with dependency: {str(e)}")
    
    def remove_dependency(self, analyzer_name: str) -> None:
        """Remove analyzer dependency."""
        self.dependencies.discard(analyzer_name)  # Remove from dependencies
        
        # Update context
        if isinstance(self.config, EnhancedAnalysisConfig) and self.config.enable_context_integration:
            try:
                deps_list = list(self.dependencies)  # Convert to list
                self.context.set(f"{self.context_namespace}.{self.name}.dependencies", deps_list, f"{self.name}_deps")
                self.logger.debug(f"Removed dependency '{analyzer_name}' from analyzer '{self.name}'")
            except Exception as e:
                self.logger.warning(f"Failed to update context after removing dependency: {str(e)}")
    
    def _check_dependencies(self) -> List[str]:
        """Check if all dependencies are satisfied."""
        failed_dependencies = []  # List of failed dependencies
        
        for dep in self.dependencies:  # Check each dependency
            try:
                # Check if dependency analyzer has completed successfully
                completed_key = f"{self.context_namespace}.{dep}.last_execution.completed"  # Completion key
                if not self.context.get(completed_key):  # Not completed
                    failed_dependencies.append(dep)  # Add to failed list
            except Exception:
                failed_dependencies.append(dep)  # Add to failed list on error
        
        return failed_dependencies  # Return list of failed dependencies
    
    def send_message(self, target_analyzer: str, message: Any) -> None:
        """Send message to another analyzer."""
        if not isinstance(self.config, EnhancedAnalysisConfig) or not self.config.enable_inter_analyzer_communication:
            return  # Communication disabled
        
        try:
            # Store message in context for target analyzer
            message_key = f"{self.context_namespace}.messages.{target_analyzer}.{int(time.time() * 1000)}"
            message_data = {
                'from': self.name,  # Sender identifier
                'to': target_analyzer,  # Target identifier  
                'message': message,  # Message content
                'timestamp': datetime.now().isoformat(),  # Send timestamp
                'message_id': message_key  # Unique message ID
            }
            
            self.context.set(message_key, message_data, f"{self.name}_message")
            self.logger.debug(f"Sent message from '{self.name}' to '{target_analyzer}'")
        except Exception as e:
            self.logger.warning(f"Failed to send message: {str(e)}")
    
    def receive_messages(self) -> List[Any]:
        """Receive messages from other analyzers."""
        messages = []  # List of received messages
        
        if not isinstance(self.config, EnhancedAnalysisConfig) or not self.config.enable_inter_analyzer_communication:
            return messages  # Communication disabled
        
        try:
            # Get messages for this analyzer
            message_prefix = f"{self.context_namespace}.messages.{self.name}."
            all_keys = self.context.keys()  # Get all context keys
            
            for key in all_keys:  # Check each key
                if key.startswith(message_prefix):  # Message for this analyzer
                    try:
                        message_data = self.context.get(key)  # Get message data
                        if message_data and isinstance(message_data, dict):
                            messages.append(message_data)  # Add to messages list
                    except Exception:
                        pass  # Skip invalid messages
            
            if messages:
                self.logger.debug(f"Received {len(messages)} messages for analyzer '{self.name}'")
        except Exception as e:
            self.logger.warning(f"Failed to receive messages: {str(e)}")
        
        return messages  # Return received messages
    
    def share_data(self, data_key: str, data: Any) -> None:
        """Share data with other analyzers."""
        try:
            # Store shared data in context
            shared_key = f"{self.context_namespace}.shared_data.{data_key}"
            shared_info = {
                'data': data,  # Actual data
                'shared_by': self.name,  # Analyzer that shared data
                'shared_at': datetime.now().isoformat(),  # Share timestamp
                'data_type': type(data).__name__  # Data type information
            }
            
            self.context.set(shared_key, shared_info, f"{self.name}_share")
            self.logger.debug(f"Shared data key '{data_key}' from analyzer '{self.name}'")
        except Exception as e:
            self.logger.warning(f"Failed to share data: {str(e)}")
    
    def get_shared_data(self, data_key: str) -> Any:
        """Get shared data from other analyzers."""
        try:
            # Retrieve shared data from context
            shared_key = f"{self.context_namespace}.shared_data.{data_key}"
            shared_info = self.context.get(shared_key)  # Get shared data info
            
            if shared_info and isinstance(shared_info, dict):
                self.logger.debug(f"Retrieved shared data key '{data_key}' for analyzer '{self.name}'")
                return shared_info.get('data')  # Return actual data
            else:
                return None  # No data available
        except Exception as e:
            self.logger.warning(f"Failed to get shared data: {str(e)}")
            return None  # Return None on error
    
    @contextmanager
    def _execution_context(self, data: Any, config: EnhancedAnalysisConfig):
        """Context manager for execution tracking and cleanup."""
        execution_id = f"exec_{self.name}_{int(time.time() * 1000)}"  # Generate execution ID
        start_time = time.time()  # Record start time
        
        try:
            # Record execution start in context
            if config.enable_context_integration:
                exec_key = f"{self.context_namespace}.{self.name}.executions.{execution_id}"
                exec_info = {
                    'execution_id': execution_id,  # Unique execution ID
                    'started_at': datetime.now().isoformat(),  # Start timestamp
                    'status': 'running',  # Execution status
                    'data_type': type(data).__name__,  # Input data type
                    'config': config.to_dict()  # Configuration used
                }
                self.context.set(exec_key, exec_info, f"{self.name}_exec")
            
            yield execution_id  # Provide execution ID to caller
            
        finally:
            # Record execution completion
            end_time = time.time()  # Record end time
            execution_time = end_time - start_time  # Calculate execution time
            
            if config.enable_context_integration:
                try:
                    exec_key = f"{self.context_namespace}.{self.name}.executions.{execution_id}"
                    exec_info = self.context.get(exec_key) or {}  # Get existing info
                    exec_info.update({
                        'completed_at': datetime.now().isoformat(),  # Completion timestamp
                        'execution_time': execution_time,  # Total execution time
                        'status': 'completed'  # Update status
                    })
                    self.context.set(exec_key, exec_info, f"{self.name}_exec")
                except Exception as e:
                    self.logger.warning(f"Failed to update execution context: {str(e)}")
    
    def analyze(self, data: Any, config: Optional[EnhancedAnalysisConfig] = None) -> EnhancedAnalysisResult[Any]:
        """
        Enhanced analysis method with Context integration and advanced features.
        
        Provides comprehensive analysis workflow with dependency checking,
        Context integration, performance monitoring, and error recovery.
        
        Args:
            data: Input data for analysis
            config: Enhanced configuration override
            
        Returns:
            EnhancedAnalysisResult with comprehensive metadata and tracking
        """
        analysis_config = config or self.config  # Use provided config or instance config
        if not isinstance(analysis_config, EnhancedAnalysisConfig):
            # Convert to enhanced config if needed
            analysis_config = EnhancedAnalysisConfig.from_dict(analysis_config.to_dict())
        
        # Create enhanced result
        result = EnhancedAnalysisResult[Any](
            analyzer_name=self.name,  # Set analyzer name
            data=None,  # Will be populated by analysis
            context_namespace=analysis_config.context_namespace  # Set context namespace
        )
        
        # Use execution context manager
        with self._execution_context(data, analysis_config) as execution_id:
            result.execution_id = execution_id  # Set execution ID
            
            try:
                # Check dependencies
                failed_deps = self._check_dependencies()  # Check dependency satisfaction
                if failed_deps:  # Failed dependencies found
                    for dep in failed_deps:
                        result.add_dependency_failed(dep)  # Record failed dependency
                    
                    if not analysis_config.enable_error_recovery:  # Error recovery disabled
                        raise EnhancedAnalysisError(
                            f"Dependencies not satisfied: {failed_deps}",
                            "DEPENDENCY_FAILURE",
                            {"failed_dependencies": failed_deps},
                            self.name,
                            self.context
                        )
                
                # Perform analysis with retry logic
                for attempt in range(analysis_config.max_retry_attempts + 1):
                    try:
                        self.retry_count = attempt  # Update retry count
                        
                        # Call base analysis method
                        base_result = super().analyze(data, analysis_config)  # Call parent method
                        
                        # Transfer data to enhanced result
                        result.data = base_result.data  # Transfer analysis data
                        result.execution_time = base_result.execution_time  # Transfer execution time
                        result.statistics = base_result.statistics  # Transfer statistics
                        result.patterns = base_result.patterns  # Transfer patterns
                        result.quality_score = base_result.quality_score  # Transfer quality score
                        result.errors = base_result.errors  # Transfer errors
                        result.warnings = base_result.warnings  # Transfer warnings
                        result.success = base_result.success  # Transfer success status
                        
                        break  # Success, exit retry loop
                        
                    except Exception as e:
                        if attempt < analysis_config.max_retry_attempts:  # More attempts available
                            self.logger.warning(f"Analysis attempt {attempt + 1} failed, retrying: {str(e)}")
                            time.sleep(analysis_config.retry_delay_seconds)  # Wait before retry
                            continue  # Retry
                        else:
                            # Final attempt failed
                            error = EnhancedAnalysisError(
                                f"Analysis failed after {analysis_config.max_retry_attempts + 1} attempts: {str(e)}",
                                "ANALYSIS_FAILURE",
                                {"attempts": analysis_config.max_retry_attempts + 1, "original_error": str(e)},
                                self.name,
                                self.context
                            )
                            self.last_error = error  # Store last error
                            raise error  # Raise enhanced error
                
                # Record successful execution in context
                if analysis_config.enable_context_integration:
                    try:
                        self.context.set(f"{self.context_namespace}.{self.name}.last_execution.completed", True, f"{self.name}_complete")
                        self.context.set(f"{self.context_namespace}.{self.name}.last_execution.result", result.to_dict(), f"{self.name}_result")
                        
                        # Record context keys accessed during analysis
                        result.add_context_key_created(f"{self.context_namespace}.{self.name}.last_execution.completed")
                        result.add_context_key_created(f"{self.context_namespace}.{self.name}.last_execution.result")
                    except Exception as e:
                        self.logger.warning(f"Failed to update context with execution results: {str(e)}")
                
                self.logger.info(f"Enhanced analysis completed successfully for analyzer '{self.name}'")
                
            except Exception as e:
                # Enhanced error handling
                if isinstance(e, EnhancedAnalysisError):
                    result.add_error(str(e))  # Add enhanced error
                else:
                    enhanced_error = EnhancedAnalysisError(
                        f"Analysis failed: {str(e)}",
                        "ANALYSIS_ERROR",
                        {"original_error": str(e)},
                        self.name,
                        self.context
                    )
                    result.add_error(str(enhanced_error))  # Add converted error
                
                self.logger.error(f"Enhanced analysis failed for analyzer '{self.name}': {str(e)}")
        
        return result  # Return enhanced result
    
    def _analyze_impl(self, data: Any, config: EnhancedAnalysisConfig) -> Any:
        """
        Default implementation for enhanced analyzer.
        
        This provides a basic implementation that can be overridden by subclasses.
        For testing and base functionality.
        
        Args:
            data: Input data for analysis
            config: Enhanced analysis configuration
            
        Returns:
            Basic analysis result
        """
        # Provide basic analysis result
        return {
            'analyzer_type': 'enhanced_base',  # Analyzer type identifier
            'data_type': type(data).__name__,  # Input data type
            'data_size': len(str(data)),  # Rough data size estimate
            'timestamp': datetime.now().isoformat(),  # Analysis timestamp
            'config_used': config.context_namespace,  # Configuration namespace
            'enhanced_features': {
                'context_integration': config.enable_context_integration,  # Context integration status
                'performance_monitoring': config.enable_performance_monitoring,  # Performance monitoring status
                'error_recovery': config.enable_error_recovery  # Error recovery status
            }
        }


class EnhancedAnalysisRegistry(AnalysisRegistry):
    """
    Enhanced registry with Context integration and advanced features.
    
    Extends base registry with Context system integration, dependency management,
    and advanced analyzer lifecycle management.
    """
    
    @staticmethod
    def create_enhanced_pipeline(analyzer_configs: List[Dict[str, Any]], 
                                context: Optional[Context] = None,
                                pipeline_name: str = "enhanced_pipeline") -> List[EnhancedAnalyzerV2]:
        """
        Create enhanced analyzer pipeline with dependency resolution and Context integration.
        
        Args:
            analyzer_configs: List of analyzer configuration dictionaries
            context: Shared context instance (creates if None)
            pipeline_name: Name for the pipeline
            
        Returns:
            List of configured enhanced analyzer instances in execution order
        """
        logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")
        
        # Initialize shared context
        shared_context = context or Context(enable_history=True, enable_metrics=True)
        
        # Create analyzers
        analyzers = []
        for i, config_dict in enumerate(analyzer_configs):
            try:
                # Extract analyzer information
                analyzer_name = config_dict.get('name', f"analyzer_{i}")
                analyzer_type = config_dict.get('type', 'enhanced_summarizer')
                
                # Create enhanced configuration
                enhanced_config = EnhancedAnalysisConfig.from_dict(config_dict.get('config', {}))
                enhanced_config.enable_pipeline_mode = True
                enhanced_config.pipeline_name = pipeline_name
                
                # Get analyzer class from registry
                analyzer_info = AnalysisRegistry.get_analyzer_info(analyzer_type)
                if not analyzer_info:
                    logger.error(f"Analyzer type '{analyzer_type}' not found in registry")
                    continue
                
                # Create analyzer instance
                analyzer_class = analyzer_info['class']
                if issubclass(analyzer_class, EnhancedAnalyzerV2):
                    analyzer = analyzer_class(analyzer_name, enhanced_config, shared_context)
                else:
                    # Wrap base analyzer
                    analyzer = EnhancedAnalyzerV2(analyzer_name, enhanced_config, shared_context)
                
                # Set up dependencies
                dependencies = config_dict.get('dependencies', [])
                for dep in dependencies:
                    analyzer.add_dependency(dep)
                
                analyzers.append(analyzer)
                logger.info(f"Created enhanced analyzer '{analyzer_name}' for pipeline '{pipeline_name}'")
                
            except Exception as e:
                logger.error(f"Failed to create analyzer {i}: {str(e)}")
        
        logger.info(f"Created enhanced pipeline '{pipeline_name}' with {len(analyzers)} analyzers")
        return analyzers


# Enhanced analyzer factory function
def create_enhanced_analyzer(analyzer_type: str, name: str, 
                           config: Optional[EnhancedAnalysisConfig] = None,
                           context: Optional[Context] = None) -> EnhancedAnalyzerV2:
    """
    Create enhanced analyzer instance with Context integration.
    
    Args:
        analyzer_type: Type of analyzer to create
        name: Name for analyzer instance
        config: Enhanced configuration
        context: Context instance for integration
        
    Returns:
        Configured enhanced analyzer instance
    """
    # Get analyzer info from registry
    analyzer_info = AnalysisRegistry.get_analyzer_info(analyzer_type)
    if not analyzer_info:
        raise EnhancedAnalysisError(
            f"Analyzer type '{analyzer_type}' not found",
            "ANALYZER_NOT_FOUND"
        )
    
    # Create configuration
    enhanced_config = config or EnhancedAnalysisConfig()
    shared_context = context or Context(enable_history=True, enable_metrics=True)
    
    # Create analyzer instance
    analyzer_class = analyzer_info['class']
    if issubclass(analyzer_class, EnhancedAnalyzerV2):
        return analyzer_class(name, enhanced_config, shared_context)
    else:
        # Wrap base analyzer in enhanced wrapper
        return EnhancedAnalyzerV2(name, enhanced_config, shared_context)


# Export enhanced components
__all__ = [
    'EnhancedAnalysisError',
    'EnhancedAnalysisConfig', 
    'EnhancedAnalysisResult',
    'EnhancedAnalyzerV2',
    'EnhancedAnalysisRegistry',
    'create_enhanced_analyzer'
]