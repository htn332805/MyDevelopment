#!/usr/bin/env python3
"""
Exercise 5D Error Handling & Recovery Framework - Integration Test

Simple test to validate that all components can be imported and work together
when used as a module within the Framework0 ecosystem.
"""

def test_framework_imports():
    """Test that all error handling components can be imported."""
    print("🔧 Testing Exercise 5D Error Handling Framework Integration...")
    
    try:
        # Test core imports
        from scriptlets.foundation.errors.error_core import (
            ErrorConfiguration, ErrorCategory, ErrorSeverity, 
            ErrorContext, RecoveryAction
        )
        print("✓ Core error handling components imported successfully")
        
        # Test error processing imports
        from scriptlets.foundation.errors.error_handlers import (
            ErrorDetector, ErrorClassifier, ErrorRouter, 
            ErrorAggregator, ErrorNotifier
        )
        print("✓ Error processing engine imported successfully")
        
        # Test recovery strategy imports
        from scriptlets.foundation.errors.recovery_strategies import (
            RetryStrategy, CircuitBreaker, FallbackStrategy, RecoveryOrchestrator
        )
        print("✓ Recovery automation imported successfully")
        
        # Test resilience pattern imports
        from scriptlets.foundation.errors.resilience_patterns import (
            BulkheadIsolation, TimeoutManager, ResilienceMetrics,
            BulkheadState, ResourceState
        )
        print("✓ Advanced resilience patterns imported successfully")
        
        # Test module-level imports
        import scriptlets.foundation.errors as error_framework
        print("✓ Complete error framework module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_component_initialization():
    """Test that components can be initialized with default configuration."""
    print("\n🔧 Testing component initialization...")
    
    try:
        from scriptlets.foundation.errors.error_core import ErrorConfiguration
        from scriptlets.foundation.errors.error_handlers import ErrorDetector
        from scriptlets.foundation.errors.recovery_strategies import RetryStrategy
        from scriptlets.foundation.errors.resilience_patterns import TimeoutManager
        
        # Create default configuration
        config = ErrorConfiguration()
        print("✓ Default error configuration created")
        
        # Initialize core components
        detector = ErrorDetector(config)
        print("✓ Error detector initialized")
        
        retry_strategy = RetryStrategy()
        print("✓ Retry strategy initialized")
        
        timeout_manager = TimeoutManager(config)
        print("✓ Timeout manager initialized")
        
        # Test basic functionality
        stats = detector.get_stats()
        assert isinstance(stats, dict)
        print("✓ Component statistics accessible")
        
        return True
        
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False

def test_framework_integration():
    """Test Framework0 integration capabilities."""
    print("\n🔧 Testing Framework0 integration...")
    
    try:
        from scriptlets.foundation.errors import create_error_context
        
        # Test convenience function
        context = create_error_context(
            category="SYSTEM",
            severity="HIGH", 
            message="Test error for integration",
            details={"test": True}
        )
        
        print("✓ Error context creation successful")
        print(f"  - Error ID: {context.error_id}")
        print(f"  - Timestamp: {context.timestamp}")
        print(f"  - Category: {context.category}")
        
        # Test serialization
        serialized = context.to_dict()
        assert isinstance(serialized, dict)
        print("✓ Error context serialization successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Exercise 5D Error Handling & Recovery Framework")
    print("Integration Test Suite")
    print("=" * 60)
    
    tests = [
        test_framework_imports,
        test_component_initialization,
        test_framework_integration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Framework is ready for use!")
        print("\nFramework Components:")
        print("  • Error Core Infrastructure (error_core.py)")
        print("  • Error Processing Engine (error_handlers.py)")
        print("  • Recovery Automation (recovery_strategies.py)")
        print("  • Advanced Resilience Patterns (resilience_patterns.py)")
        print("  • Main Orchestration Scriptlet (error_handling.py)")
        print("\nFramework0 Foundation Status:")
        print("  • 5A: Logging & Monitoring ✓")
        print("  • 5B: Health Monitoring ✓")
        print("  • 5C: Performance Metrics ✓")
        print("  • 5D: Error Handling & Recovery ✓ (COMPLETED)")
    else:
        print(f"⚠️  {total - passed} tests failed - Review implementation")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)