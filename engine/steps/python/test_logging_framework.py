#!/usr/bin/env python3
"""
Foundation Logging Framework Test Scriptlet

Tests the modular logging framework components in Framework0.
Validates imports, basic functionality, and Framework0 integration.

Author: Framework0 System
Version: 1.0.0
"""

import logging
from typing import Dict, Any

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


class TestLoggingFramework(BaseScriptlet):
    """
    Test scriptlet for validating the modular logging framework.
    
    This scriptlet tests all components of the foundation logging system:
    - Core infrastructure imports
    - Formatter functionality  
    - Adapter integration
    - Main logging framework setup
    """
    
    def __init__(self):
        """Initialize the test scriptlet with logging setup."""
        super().__init__()
        # Get logger for this test scriptlet
        self.logger = logging.getLogger(__name__)
        
    def run(self, context, args, **kwargs) -> int:
        """
        Execute the logging framework tests.
        
        Args:
            context: Framework0 context client for state management
            args: Arguments from recipe configuration
            **kwargs: Additional test configuration arguments
            
        Returns:
            int: 0 for success, 1 for failure (Framework0 standard)
        """
        # Extract test configuration from arguments
        test_type = args.get('test_type', 'import_validation')
        
        self._log_info(f"Starting logging framework test: {test_type}")
        
        try:
            # Initialize test results container
            test_results = {
                'test_type': test_type,
                'status': 'running',
                'tests_passed': 0,
                'tests_total': 0,
                'import_validation': {},
                'functionality_tests': {},
                'framework_integration': {}
            }
            
            # Execute the requested test type
            if test_type == 'import_validation':
                # Test module imports and basic structure
                test_results = self._test_imports(test_results)
                
            elif test_type == 'functionality_test':
                # Test logging functionality and outputs
                test_results = self._test_functionality(test_results)
                
            elif test_type == 'framework_integration':
                # Test Framework0 context integration
                test_results = self._test_framework_integration(test_results, context)
                
            else:
                # Run complete validation suite
                test_results = self._run_full_validation(test_results, context)
            
            # Calculate final test status
            success_rate = (test_results['tests_passed'] / 
                            max(test_results['tests_total'], 1))
            
            test_results['status'] = 'passed' if success_rate >= 0.8 else 'failed'
            test_results['success_rate'] = success_rate
            
            # Log final results
            self._log_info(f"Test completed: {test_results['tests_passed']}/" +
                           f"{test_results['tests_total']} passed")
            
            # Store results in Framework0 context
            context.set('logging_test.results', test_results)
            context.set('logging_test.import_success', 
                        test_results['status'] == 'passed')
            
            return 0 if test_results['status'] == 'passed' else 1
            
        except Exception as e:
            # Handle test execution errors
            self._log_error(f"Test execution failed: {e}")
            
            error_results = {
                'status': 'error',
                'error_message': str(e),
                'test_type': test_type
            }
            
            context.set('logging_test.error', error_results)
            
            return 1  # Error exit code
    
    def _test_imports(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test all logging framework module imports.
        
        Args:
            results: Current test results dictionary
            
        Returns:
            Updated results with import test outcomes
        """
        self._log_info("Testing module imports...")
        
        import_tests = [
            ('core', 'scriptlets.foundation.logging.core'),
            ('formatters', 'scriptlets.foundation.logging.formatters'), 
            ('adapters', 'scriptlets.foundation.logging.adapters'),
            ('main_init', 'scriptlets.foundation.logging'),
            ('framework_scriptlet', 'scriptlets.foundation.logging_framework')
        ]
        
        import_results = {}
        passed_imports = 0
        
        for test_name, module_path in import_tests:
            try:
                # Attempt to import the module
                __import__(module_path)
                import_results[test_name] = {'status': 'success', 'module': module_path}
                passed_imports += 1
                self._log_info(f"Import success: {module_path}")
                
            except ImportError as e:
                # Record import failure
                import_results[test_name] = {
                    'status': 'failed',
                    'module': module_path,
                    'error': str(e)
                }
                self._log_error(f"Import failed: {module_path} - {e}")
        
        # Update results
        results['import_validation'] = import_results
        results['tests_passed'] += passed_imports
        results['tests_total'] += len(import_tests)
        
        self._log_info(f"Import tests: {passed_imports}/{len(import_tests)} passed")
        
        return results
    
    def _test_functionality(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test basic logging functionality.
        
        Args:
            results: Current test results dictionary
            
        Returns:
            Updated results with functionality test outcomes
        """
        self._log_info("Testing logging functionality...")
        
        functionality_tests = {}
        passed_tests = 0
        
        try:
            # Test 1: Logger creation
            from scriptlets.foundation.logging import get_framework_logger
            test_logger = get_framework_logger('functionality_test')
            functionality_tests['logger_creation'] = {'status': 'success'}
            passed_tests += 1
            
        except Exception as e:
            functionality_tests['logger_creation'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 2: Basic logging operations
            test_logger.info("Test info message")
            test_logger.debug("Test debug message") 
            test_logger.warning("Test warning message")
            functionality_tests['basic_logging'] = {'status': 'success'}
            passed_tests += 1
            
        except Exception as e:
            functionality_tests['basic_logging'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 3: Configuration loading
            from scriptlets.foundation.logging.core import get_default_logging_config
            config = get_default_logging_config()
            functionality_tests['config_loading'] = {
                'status': 'success',
                'config_sections': len(config) if config else 0
            }
            passed_tests += 1
            
        except Exception as e:
            functionality_tests['config_loading'] = {'status': 'failed', 'error': str(e)}
        
        # Update results
        results['functionality_tests'] = functionality_tests
        results['tests_passed'] += passed_tests
        results['tests_total'] += 3
        
        self._log_info(f"Functionality tests: {passed_tests}/3 passed")
        
        return results
    
    def _test_framework_integration(self, results: Dict[str, Any], context) -> Dict[str, Any]:
        """
        Test Framework0 integration features.
        
        Args:
            results: Current test results dictionary
            context: Framework0 context client
            
        Returns:
            Updated results with integration test outcomes
        """
        self._log_info("Testing Framework0 integration...")
        
        integration_tests = {}
        passed_tests = 0
        
        try:
            # Test 1: Context integration
            context.set('test.logging_integration', True)
            retrieved_value = context.get('test.logging_integration')
            integration_tests['context_integration'] = {
                'status': 'success' if retrieved_value else 'failed',
                'value': retrieved_value
            }
            if retrieved_value:
                passed_tests += 1
                
        except Exception as e:
            integration_tests['context_integration'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 2: Logger adapter functionality  
            from scriptlets.foundation.logging.adapters import LoggerManager
            logger_manager = LoggerManager()
            test_logger = logger_manager.get_logger('integration_test')
            test_logger.info("Framework0 integration test message")
            integration_tests['adapter_functionality'] = {'status': 'success'}
            passed_tests += 1
            
        except Exception as e:
            integration_tests['adapter_functionality'] = {'status': 'failed', 'error': str(e)}
        
        # Update results
        results['framework_integration'] = integration_tests
        results['tests_passed'] += passed_tests
        results['tests_total'] += 2
        
        self._log_info(f"Integration tests: {passed_tests}/2 passed")
        
        return results
    
    def _run_full_validation(self, results: Dict[str, Any], context) -> Dict[str, Any]:
        """
        Run complete validation suite.
        
        Args:
            results: Current test results dictionary
            context: Framework0 context client
            
        Returns:
            Complete test results
        """
        self._log_info("Running full validation suite...")
        
        # Execute all test categories
        results = self._test_imports(results)
        results = self._test_functionality(results)
        results = self._test_framework_integration(results, context)
        
        self._log_info("Full validation completed")
        
        return results
    
    def _log_info(self, message: str) -> None:
        """Log info message using available logger."""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"INFO: TestLoggingFramework: {message}")
    
    def _log_error(self, message: str) -> None:
        """Log error message using available logger."""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"ERROR: TestLoggingFramework: {message}")