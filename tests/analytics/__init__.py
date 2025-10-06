#!/usr/bin/env python3
"""
Analytics Tests Module - Test Suite for Exercise 7 Recipe Analytics

Comprehensive test suite for validating Exercise 7 Recipe Analytics system
functionality, performance, and integration.

Test Modules:
- test_exercise_7_analytics: Main test suite with comprehensive coverage

Usage:
    # Run all analytics tests
    python -m pytest tests/analytics/
    
    # Run specific test categories
    python -m pytest tests/analytics/ -m integration
    python -m pytest tests/analytics/ -m performance

Author: Framework0 Development Team
Version: 1.0.0
"""

from src.core.logger import get_logger

logger = get_logger(__name__)

__version__ = "1.0.0"
__author__ = "Framework0 Development Team"

logger.info("Analytics tests module initialized")