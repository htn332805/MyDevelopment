#!/usr/bin/env python3
"""
Comprehensive Test Runner for MyDevelopment Framework.

This script runs all unit tests and integration tests for the framework,
providing a comprehensive overview of code quality and functionality.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any
import json
import time
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set up environment
os.environ['PYTHONPATH'] = str(project_root) + ':' + os.environ.get('PYTHONPATH', '')

class ComprehensiveTestRunner:
    """Comprehensive test runner for the entire framework."""
    
def __init__(self) -> Any:
    # Execute __init__ operation
    """Initialize the test runner."""
    self.project_root = project_root
        self.test_results = {
            'start_time': None,
            'end_time': None,
            'total_duration': 0,
            'test_suites': {},
            'summary': {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'skipped': 0,
                'success_rate': 0.0
            }
        }
        
        # Define test suites to run
        self.test_suites = {
            'Unit Tests - Core Framework': [
                'tests/unit/test_context.py',
                'tests/unit/test_context_v2.py::TestContextV2Basics',
                'tests/unit/test_runner.py', 
                'tests/unit/test_error_handling.py::TestAdvancedErrorHandler',
                'tests/unit/test_enhanced_framework.py::TestInterfaces',
            ],
            'Unit Tests - Data Processing': [
                'tests/test_csv_reader.py',
            ],
            'Unit Tests - Excel Processing': [
                'tests/test_excel_processor.py',
            ],
            'Integration Tests': [
                'tests/integration/test_example_numbers.py',
            ],
            'Application Tests': [
                'tests/test_quiz_dashboard.py::TestQuizDatabase::test_question_crud_operations',
                'tests/test_recipe_packager.py',
            ],
            'Custom Test Runners': [
                'tests/run_visual_recipe_tests.py',
            ]
        }
        
    def run_pytest_suite(self, test_paths: List[str], suite_name: str) -> Dict[str, Any]:
        # Execute run_pytest_suite operation
    """Run a pytest suite and return results."""
    print(f"\n{'='*60}")
        print(f"Running {suite_name}")
        print(f"{'='*60}")
        
        suite_result = {
            'name': suite_name,
            'start_time': time.time(),
            'tests': [],
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'duration': 0,
            'success': True
        }
        
        for test_path in test_paths:
            print(f"\nRunning: {test_path}")
            
            try:
                # Run pytest with JSON report
                cmd = [
                    sys.executable, '-m', 'pytest', 
                    test_path, 
                    '-v',
                    '--tb=short',
                    '--maxfail=5'
                ]
                
                result = subprocess.run(
                    cmd,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=60  # 60 second timeout per test file
                )
                
                test_result = {
                    'path': test_path,
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'success': result.returncode == 0
                }
                
                suite_result['tests'].append(test_result)
                
                # Parse output for basic stats
                if result.returncode == 0:
                    print(f"✅ PASSED: {test_path}")
                    # Try to extract number of passed tests
                    if ' passed' in result.stdout:
                        try:
                            passed_line = [line for line in result.stdout.split('\n') 
                                         if ' passed' in line and '=' in line][-1]
                            if 'passed' in passed_line:
                                passed_count = int(passed_line.split()[0])
                                suite_result['passed'] += passed_count
                        except:
                            suite_result['passed'] += 1
                else:
                    print(f"❌ FAILED: {test_path}")
                    suite_result['failed'] += 1
                    suite_result['success'] = False
                    
                    # Print error details
                    if result.stderr:
                        print(f"   Error: {result.stderr.split(chr(10))[0]}")
                    
            except subprocess.TimeoutExpired:
                print(f"⏰ TIMEOUT: {test_path}")
                suite_result['errors'] += 1
                suite_result['success'] = False
                
                test_result = {
                    'path': test_path,
                    'returncode': -1,
                    'stdout': '',
                    'stderr': 'Test timed out after 60 seconds',
                    'success': False
                }
                suite_result['tests'].append(test_result)
                
            except Exception as e:
                print(f"🔥 ERROR: {test_path} - {e}")
                suite_result['errors'] += 1
                suite_result['success'] = False
                
                test_result = {
                    'path': test_path,
                    'returncode': -2,
                    'stdout': '',
                    'stderr': str(e),
                    'success': False
                }
                suite_result['tests'].append(test_result)
        
        suite_result['duration'] = time.time() - suite_result['start_time']
        return suite_result
    
    def run_custom_test(self, test_script: str, suite_name: str) -> Dict[str, Any]:
        # Execute run_custom_test operation
    """Run a custom test script."""
    print(f"\n{'='*60}")
        print(f"Running Custom Test: {suite_name}")
        print(f"{'='*60}")
        
        suite_result = {
            'name': suite_name,
            'start_time': time.time(),
            'tests': [],
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'duration': 0,
            'success': True
        }
        
        try:
            cmd = [sys.executable, test_script]
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout for custom tests
            )
            
            test_result = {
                'path': test_script,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            suite_result['tests'].append(test_result)
            
            if result.returncode == 0:
                print(f"✅ PASSED: {test_script}")
                suite_result['passed'] += 1
                # Print success output
                print(result.stdout)
            else:
                print(f"❌ FAILED: {test_script}")
                suite_result['failed'] += 1
                suite_result['success'] = False
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"🔥 ERROR: {test_script} - {e}")
            suite_result['errors'] += 1
            suite_result['success'] = False
            
        suite_result['duration'] = time.time() - suite_result['start_time']
        return suite_result
    
    def run_all_tests(self) -> Dict[str, Any]:
        # Execute run_all_tests operation
    """Run all test suites."""
    print("🚀 Starting Comprehensive Test Suite")
        print(f"Project Root: {self.project_root}")
        print(f"Python Path: {os.environ.get('PYTHONPATH', 'Not Set')}")
        
        self.test_results['start_time'] = time.time()
        
        # Run pytest suites
        for suite_name, test_paths in self.test_suites.items():
            if suite_name == 'Custom Test Runners':
                # Handle custom test runners separately
                for test_script in test_paths:
                    custom_result = self.run_custom_test(test_script, test_script)
                    self.test_results['test_suites'][test_script] = custom_result
            else:
                # Regular pytest suites
                suite_result = self.run_pytest_suite(test_paths, suite_name)
                self.test_results['test_suites'][suite_name] = suite_result
        
        self.test_results['end_time'] = time.time()
        self.test_results['total_duration'] = (
            self.test_results['end_time'] - self.test_results['start_time']
        )
        
        # Calculate summary
        self._calculate_summary()
        
        return self.test_results
    
def _calculate_summary(self) -> Any:
    # Execute _calculate_summary operation
    """Calculate test summary statistics."""
    summary = self.test_results['summary']
        
        for suite_name, suite_result in self.test_results['test_suites'].items():
            summary['total_tests'] += len(suite_result['tests'])
            summary['passed'] += suite_result['passed']
            summary['failed'] += suite_result['failed'] 
            summary['errors'] += suite_result['errors']
            summary['skipped'] += suite_result['skipped']
        
        total_run = summary['passed'] + summary['failed'] + summary['errors']
        if total_run > 0:
            summary['success_rate'] = (summary['passed'] / total_run) * 100
        else:
            summary['success_rate'] = 0.0
    
def print_summary(self) -> Any:
    # Execute print_summary operation
    """Print test summary."""
    print(f"\n{'='*80}")
        print("🎯 COMPREHENSIVE TEST RESULTS SUMMARY")
        print(f"{'='*80}")
        
        print(f"⏱️  Total Duration: {self.test_results['total_duration']:.2f} seconds")
        print(f"🧪 Total Test Suites: {len(self.test_results['test_suites'])}")
        
        summary = self.test_results['summary']
        print(f"📊 Test Statistics:")
        print(f"   • Total Tests: {summary['total_tests']}")
        print(f"   • Passed: {summary['passed']} ✅")
        print(f"   • Failed: {summary['failed']} ❌")
        print(f"   • Errors: {summary['errors']} 🔥")
        print(f"   • Skipped: {summary['skipped']} ⏭️")
        print(f"   • Success Rate: {summary['success_rate']:.1f}%")
        
        print(f"\n📋 Suite-by-Suite Results:")
        for suite_name, suite_result in self.test_results['test_suites'].items():
            status = "✅ PASS" if suite_result['success'] else "❌ FAIL"
            duration = suite_result['duration']
            test_count = len(suite_result['tests'])
            print(f"   {status} {suite_name} ({test_count} tests, {duration:.1f}s)")
        
        # Overall status
        overall_success = summary['failed'] == 0 and summary['errors'] == 0
        overall_status = "🎉 ALL TESTS PASSED" if overall_success else "⚠️  SOME TESTS FAILED"
        
        print(f"\n{overall_status}")
        print(f"{'='*80}")
        
        return overall_success
    
def save_results(e: str  = 'test_results.json') -> Any::
    # Execute save_results operation
        """Save test results to JSON file."""
        try:
            output_path = self.project_root / output_file
            with open(output_path, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            print(f"💾 Test results saved to: {output_path}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")


def main() -> Any:
    # Execute main operation
    """Main function to run comprehensive tests."""
    runner = ComprehensiveTestRunner()
    
    try:
        # Run all tests
        results = runner.run_all_tests()
        
        # Print summary
        success = runner.print_summary()
        
        # Save results
        runner.save_results()
        
        # Return appropriate exit code
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Test run interrupted by user")
        return 2
    except Exception as e:
        print(f"\n🔥 Test run failed with error: {e}")
        return 3


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)