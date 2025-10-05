#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Runner for Delta Compression Module.

This script runs the test suite for the delta compression module.
"""
import os
import sys
import pytest

# Set debug mode for verbose output
os.environ['DEBUG'] = '1'

if __name__ == "__main__":
    # Run the tests
    test_file = "tests/test_delta_compression.py"
    sys.exit(pytest.main(["-v", test_file]))