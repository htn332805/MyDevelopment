#!/usr/bin/env python3
"""
Framework0 Foundation - Health Monitoring Test Scriptlet

Tests the health monitoring system components in Framework0.
Validates health checks, metric collection, alerting, and Framework0 integration.

Author: Framework0 System
Version: 1.0.0
"""

import time
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


class TestHealthMonitoringScriptlet(BaseScriptlet):
    """
    Test scriptlet for validating the health monitoring system.
    
    This scriptlet tests all components of the health monitoring system:
    - Core infrastructure and configuration
    - System health checks (CPU, memory, disk, network)
    - Metric collection and analysis
    - Threshold monitoring and alerting
    - Framework0 integration
    """
    
    def __init__(self):
        """Initialize the health monitoring test scriptlet."""
        super().__init__()
        
    def run(self, context, args, **kwargs) -> int:
        """
        Execute the health monitoring system tests.
        
        Args:
            context: Framework0 context client for state management
            args: Arguments from recipe configuration
            **kwargs: Additional test configuration arguments
            
        Returns:
            int: 0 for success, 1 for failure (Framework0 standard)
        """
        # Extract test configuration from arguments
        test_type = args.get('test_type', 'import_validation')
        
        self._log_info(f"Starting health monitoring test: {test_type}")
        
        try:
            # Initialize test results container
            test_results = {
                'test_type': test_type,
                'status': 'running',
                'tests_passed': 0,
                'tests_total': 0,
                'import_validation': {},
                'health_checks': {},
                'integration_tests': {}
            }
            
            # Execute the requested test type
            if test_type == 'import_validation':
                test_results = self._test_imports(test_results)
                
            elif test_type == 'health_checks':
                test_results = self._test_health_checks(test_results)
                
            elif test_type == 'integration_test':
                test_results = self._test_framework_integration(test_results, context)
                
            elif test_type == 'full_validation':
                # Run complete validation suite
                test_results = self._run_full_validation(test_results, context)
            
            else:
                self._log_error(f"Unknown test type: {test_type}")
                return 1
            
            # Calculate final test status
            success_rate = (test_results['tests_passed'] / 
                            max(test_results['tests_total'], 1))
            
            test_results['status'] = 'passed' if success_rate >= 0.8 else 'failed'
            test_results['success_rate'] = success_rate
            
            # Log final results
            self._log_info(f"Test completed: {test_results['tests_passed']}/" +
                           f"{test_results['tests_total']} passed")
            
            # Store results in Framework0 context
            context.set('health_test.results', test_results)
            context.set('health_test.success', test_results['status'] == 'passed')
            
            return 0 if test_results['status'] == 'passed' else 1
            
        except Exception as e:
            # Handle test execution errors
            self._log_error(f"Test execution failed: {e}")
            
            error_results = {
                'status': 'error',
                'error_message': str(e),
                'test_type': test_type
            }
            
            context.set('health_test.error', error_results)
            
            return 1  # Error exit code
    
    def _test_imports(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test all health monitoring module imports.
        
        Args:
            results: Current test results dictionary
            
        Returns:
            Updated results with import test outcomes
        """
        self._log_info("Testing module imports...")
        
        import_tests = [
            ('health_core', 'scriptlets.foundation.health.health_core'),
            ('health_checks', 'scriptlets.foundation.health.health_checks'), 
            ('health_reporters', 'scriptlets.foundation.health.health_reporters'),
            ('health_init', 'scriptlets.foundation.health'),
            ('health_monitoring', 'scriptlets.foundation.health_monitoring')
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
    
    def _test_health_checks(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test health check functionality.
        
        Args:
            results: Current test results dictionary
            
        Returns:
            Updated results with health check test outcomes
        """
        self._log_info("Testing health check functionality...")
        
        health_check_tests = {}
        passed_tests = 0
        
        try:
            # Test 1: Health monitor creation
            from scriptlets.foundation.health import get_health_monitor
            health_monitor = get_health_monitor('test_monitor')
            health_check_tests['monitor_creation'] = {'status': 'success'}
            passed_tests += 1
            
        except Exception as e:
            health_check_tests['monitor_creation'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 2: System resource checking
            results_list = health_monitor.check_system_health()
            if results_list and len(results_list) > 0:
                health_check_tests['system_checks'] = {
                    'status': 'success',
                    'checks_run': len(results_list)
                }
                passed_tests += 1
            else:
                health_check_tests['system_checks'] = {
                    'status': 'failed',
                    'error': 'No health check results returned'
                }
            
        except Exception as e:
            health_check_tests['system_checks'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 3: Health status determination
            overall_status = health_monitor.get_health_status()
            health_check_tests['status_determination'] = {
                'status': 'success',
                'overall_status': overall_status.value
            }
            passed_tests += 1
            
        except Exception as e:
            health_check_tests['status_determination'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 4: Health report generation
            report = health_monitor.generate_health_report('text')
            if report and len(report) > 0:
                health_check_tests['report_generation'] = {
                    'status': 'success',
                    'report_length': len(report)
                }
                passed_tests += 1
            else:
                health_check_tests['report_generation'] = {
                    'status': 'failed',
                    'error': 'Empty health report generated'
                }
            
        except Exception as e:
            health_check_tests['report_generation'] = {'status': 'failed', 'error': str(e)}
        
        # Update results
        results['health_checks'] = health_check_tests
        results['tests_passed'] += passed_tests
        results['tests_total'] += 4
        
        self._log_info(f"Health check tests: {passed_tests}/4 passed")
        
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
            context.set('test.health_integration', True)
            retrieved_value = context.get('test.health_integration')
            integration_tests['context_integration'] = {
                'status': 'success' if retrieved_value else 'failed',
                'value': retrieved_value
            }
            if retrieved_value:
                passed_tests += 1
                
        except Exception as e:
            integration_tests['context_integration'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 2: Health monitoring scriptlet instantiation
            from scriptlets.foundation.health_monitoring import HealthMonitoringScriptlet
            health_scriptlet = HealthMonitoringScriptlet()
            integration_tests['scriptlet_creation'] = {
                'status': 'success',
                'name': health_scriptlet.name,
                'version': health_scriptlet.version
            }
            passed_tests += 1
            
        except Exception as e:
            integration_tests['scriptlet_creation'] = {'status': 'failed', 'error': str(e)}
        
        try:
            # Test 3: Health check execution through scriptlet
            test_args = {
                'action': 'setup',
                'initial_check': True,
                'config': {
                    'monitoring': {'enabled': True},
                    'thresholds': {
                        'cpu_usage_total': {
                            'warning_max': 80.0,
                            'critical_max': 95.0
                        }
                    }
                }
            }
            
            result_code = health_scriptlet.run(context, test_args)
            integration_tests['scriptlet_execution'] = {
                'status': 'success' if result_code == 0 else 'failed',
                'exit_code': result_code
            }
            if result_code == 0:
                passed_tests += 1
            
        except Exception as e:
            integration_tests['scriptlet_execution'] = {'status': 'failed', 'error': str(e)}
        
        # Update results
        results['integration_tests'] = integration_tests
        results['tests_passed'] += passed_tests
        results['tests_total'] += 3
        
        self._log_info(f"Integration tests: {passed_tests}/3 passed")
        
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
        results = self._test_health_checks(results)
        results = self._test_framework_integration(results, context)
        
        self._log_info("Full validation completed")
        
        return results
    
    def _log_info(self, message: str) -> None:
        """Log info message using available logger."""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"INFO: TestHealthMonitoringScriptlet: {message}")
    
    def _log_error(self, message: str) -> None:
        """Log error message using available logger."""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"ERROR: TestHealthMonitoringScriptlet: {message}")