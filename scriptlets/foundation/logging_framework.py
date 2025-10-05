"""
Framework0 Foundation - Main Logging Framework Scriptlet

Orchestration and integration layer for the modular logging system:
- Coordinates all logging components (core, formatters, adapters)
- Manages logging infrastructure setup and configuration
- Provides Framework0 integration and context management
- Handles log rotation, directory creation, and cleanup
"""

import os
import time
import logging
import logging.handlers
import pathlib

try:
    from scriptlets.framework import BaseScriptlet  # Framework0 base class
except ImportError:
    # Fallback base class if framework not available
    class BaseScriptlet:
        """Fallback base scriptlet class."""
        
        def __init__(self, context=None, **kwargs):
            """Initialize base scriptlet."""
            self.context = context
            self.logger = None
            
        def run(self, **kwargs):
            """Run method must be implemented by subclasses."""
            raise NotImplementedError("Scriptlet must implement run method")

from typing import Dict, Any, List, Optional

# Import our modular logging components
from .logging.core import (
    LogLevel, LogFormat, LoggingConfiguration,
    get_default_logging_config, merge_logging_configs
)
from .logging.formatters import (
    ContextAwareFormatter, AuditFormatter, PerformanceFormatter
)
from .logging.adapters import (
    Framework0LoggerAdapter, LoggerManager, create_logger_utilities
)


class LoggingFrameworkScriptlet(BaseScriptlet):
    """
    Main logging framework scriptlet for Framework0 infrastructure.
    
    Orchestrates the complete logging system setup:
    - Initializes modular logging components
    - Configures multiple output targets and formats
    - Sets up log rotation and directory management
    - Provides Framework0-aware logging utilities
    - Manages logging infrastructure lifecycle
    """
    
    def __init__(self) -> None:
        """Initialize the logging framework scriptlet."""
        super().__init__()
        self.name = "logging_framework"
        self.version = "2.0.0"  # Modular version
        self.description = "Modular production-ready logging infrastructure"
        
        # Internal state management
        self._loggers: Dict[str, logging.Logger] = {}
        self._handlers: List[logging.Handler] = []
        self._logger_manager: Optional[LoggerManager] = None
        self._configuration: Optional[LoggingConfiguration] = None
        
    def run(self, context, args, **kwargs) -> int:
        """
        Execute logging framework setup and management.
        
        Args:
            context: Framework0 context for state management 
            args: Configuration arguments for logging setup
            **kwargs: Additional keyword arguments
            
        Returns:
            int: 0 for success, 1 for failure (Framework0 standard)
        """
        # Record execution start time
        execution_start = time.time()
        
        try:
            # Log startup message using available logger
            if hasattr(self, 'logger') and self.logger:
                self.logger.info(f"Starting {self.name} v{self.version}")
                self.logger.info(f"Action: {args.get('action', 'setup')}")
            else:
                # Fallback to print if logger not available  
                print("Framework0 Modular Logging Infrastructure")
                print("Starting logging framework setup...")
                print("   Modular Architecture: ENABLED")
            
            # Extract action from parameters
            action = args.get('action', 'setup')
            
            # Initialize configuration
            default_config = get_default_logging_config()
            self._configuration = LoggingConfiguration(default_config)
            
            # Execute the requested action
            if action == 'setup':
                # Set up logging infrastructure
                result = self._setup_logging_infrastructure(context)
                
                # Store results in context
                context.set('logging.framework_initialized', True)
                context.set('logging.config_loaded', True)
                context.set('logging.setup_results', result)
                
                print("✅ Logging framework setup completed successfully")
                return 0  # Success
                
            else:
                print(f"❌ Unknown action: {action}")
                return 1  # Error
                
        except Exception as e:
            print(f"❌ Logging framework setup failed: {e}")
            return 1  # Error
    
    def _create_log_directories(self) -> List[str]:
        """Create necessary log directories."""
        directories = set()
        
        # Extract paths from configuration
        for section_name in ["framework", "audit", "performance"]:
            if self._configuration.is_section_enabled(section_name):
                config_getter = getattr(self._configuration, f"get_{section_name}_config")
                section_config = config_getter()
                file_path = section_config.get("file_path")
                if file_path:
                    directories.add(str(pathlib.Path(file_path).parent))
        
        # Create directories
        created = []
        for directory in directories:
            dir_path = pathlib.Path(directory)
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                created.append(str(dir_path))
        
        return created
    
    def _setup_logging_infrastructure(self, context) -> List[str]:
        """Setup core logging infrastructure."""
        configured_loggers = []
        
        # Setup framework logging
        if self._configuration.is_section_enabled("framework"):
            framework_config = self._configuration.get_framework_config()
            self._setup_framework_logger(framework_config)
            configured_loggers.append("framework0")
        
        # Setup audit logging
        if self._configuration.is_section_enabled("audit"):
            audit_config = self._configuration.get_audit_config()
            self._setup_audit_logger(audit_config)
            configured_loggers.append("audit")
        
        # Setup performance logging
        if self._configuration.is_section_enabled("performance"):
            perf_config = self._configuration.get_performance_config()
            self._setup_performance_logger(perf_config)
            configured_loggers.append("performance")
        
        return configured_loggers
    
    def _setup_framework_logger(self, config: Dict[str, Any]) -> None:
        """Setup main framework logger."""
        framework_logger = logging.getLogger("framework0")
        framework_logger.handlers.clear()
        
        # Set level
        log_level = getattr(LogLevel, config.get("level", "INFO").upper())
        framework_logger.setLevel(log_level.value)
        
        # Create formatters
        json_formatter = ContextAwareFormatter(LogFormat.STRUCTURED_JSON)
        text_formatter = ContextAwareFormatter(LogFormat.SIMPLE_TEXT)
        
        # Console handler
        outputs = config.get("outputs", ["console"])
        if "console" in outputs:
            import sys
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(text_formatter)
            framework_logger.addHandler(console_handler)
            self._handlers.append(console_handler)
        
        # File handler
        if "file" in outputs and config.get("file_path"):
            file_handler = logging.FileHandler(config["file_path"])
            file_handler.setFormatter(json_formatter)
            framework_logger.addHandler(file_handler)
            self._handlers.append(file_handler)
        
        self._loggers["framework0"] = framework_logger
    
    def _setup_audit_logger(self, config: Dict[str, Any]) -> None:
        """Setup audit logger."""
        audit_logger = logging.getLogger("framework0.audit")
        audit_logger.handlers.clear()
        audit_logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler(config["file_path"])
        file_handler.setFormatter(AuditFormatter())
        audit_logger.addHandler(file_handler)
        self._handlers.append(file_handler)
        
        self._loggers["audit"] = audit_logger
    
    def _setup_performance_logger(self, config: Dict[str, Any]) -> None:
        """Setup performance logger."""
        perf_logger = logging.getLogger("framework0.performance")
        perf_logger.handlers.clear()
        perf_logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler(config["file_path"])
        file_handler.setFormatter(PerformanceFormatter())
        perf_logger.addHandler(file_handler)
        self._handlers.append(file_handler)
        
        self._loggers["performance"] = perf_logger
    
    def _setup_log_rotation(self) -> int:
        """Setup log rotation for file handlers."""
        framework_config = self._configuration.get_framework_config()
        rotation_config = framework_config.get("rotation", {})
        
        if not rotation_config.get("enabled", False):
            return 0
        
        max_size_mb = rotation_config.get("max_size_mb", 100)
        max_files = rotation_config.get("max_files", 10)
        max_bytes = max_size_mb * 1024 * 1024
        
        rotation_count = 0
        
        # Replace file handlers with rotating versions
        for handler in self._handlers[:]:
            if isinstance(handler, logging.FileHandler):
                if not isinstance(handler, logging.handlers.RotatingFileHandler):
                    # Create rotating version
                    rotating_handler = logging.handlers.RotatingFileHandler(
                        handler.baseFilename, maxBytes=max_bytes, backupCount=max_files
                    )
                    rotating_handler.setLevel(handler.level)
                    rotating_handler.setFormatter(handler.formatter)
                    
                    # Replace in loggers
                    for logger_instance in self._loggers.values():
                        if handler in logger_instance.handlers:
                            logger_instance.removeHandler(handler)
                            logger_instance.addHandler(rotating_handler)
                    
                    # Update handler list
                    self._handlers.remove(handler)
                    self._handlers.append(rotating_handler)
                    rotation_count += 1
        
        return rotation_count
    
    def _test_logging_system(self, context) -> Dict[str, Any]:
        """Test the complete logging system."""
        test_results = {"passed": 0, "total": 0, "details": []}
        
        # Test framework logging
        test_results["total"] += 1
        try:
            if "framework0" in self._loggers:
                self._loggers["framework0"].info("Modular logging test - framework")
                test_results["passed"] += 1
                test_results["details"].append({"test": "framework", "status": "passed"})
        except Exception as e:
            test_results["details"].append({"test": "framework", "status": "failed"})
        
        # Test logger manager
        test_results["total"] += 1
        try:
            if self._logger_manager:
                test_logger = self._logger_manager.get_logger("test", context)
                test_logger.info("Modular logging test - manager")
                test_results["passed"] += 1
                test_results["details"].append({"test": "manager", "status": "passed"})
        except Exception as e:
            test_results["details"].append({"test": "manager", "status": "failed"})
        
        # Test utilities
        test_results["total"] += 1
        try:
            utilities = create_logger_utilities(context)
            test_adapter = utilities["get_logger"]("utilities_test")
            test_adapter.info("Modular logging test - utilities")
            test_results["passed"] += 1
            test_results["details"].append({"test": "utilities", "status": "passed"})
        except Exception as e:
            test_results["details"].append({"test": "utilities", "status": "failed"})
        
        return test_results