#!/usr/bin/env python3
# quiz-app/test_quiz_system.py

"""
Test script for the Interactive Quiz System.

This script validates all core components of the quiz system including:
- Database initialization and schema creation
- Question loading and validation
- Spaced repetition selection algorithm
- Quiz session management
- Integration with Framework0 components

Run this before starting the Dash application to ensure everything works.
"""

import sys
import os
import time
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import Framework0 components
from src.core.logger import get_logger

# Import quiz components
sys.path.append(str(project_root / "quiz-app"))
from models.storage import get_quiz_database
from utils.qloader import get_question_loader
from utils.selection import select_quiz_questions, get_spaced_repetition_selector

# Initialize logger
logger = get_logger(__name__, debug=True)


def test_database_initialization():
    """Test database initialization and schema creation."""
    logger.info("Testing database initialization...")
    
    try:
        # Get database instance
        db = get_quiz_database()
        
        # Test connection
        conn = db.get_connection()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['questions', 'users', 'attempts', 'question_stats']
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            logger.error(f"Missing database tables: {missing_tables}")
            return False
        
        logger.info("✓ Database initialization successful")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False


def test_question_loading():
    """Test question loading and validation."""
    logger.info("Testing question loading...")
    
    try:
        # Get question loader
        loader = get_question_loader()
        
        # Load questions
        total_files, total_questions, errors = loader.reload_questions()
        
        if errors:
            logger.warning(f"Question loading had {len(errors)} errors:")
            for error in errors[:5]:  # Show first 5 errors
                logger.warning(f"  - {error}")
        
        if total_questions == 0:
            logger.error("No questions were loaded")
            return False
        
        # Test question retrieval
        all_questions = loader.get_questions_by_criteria()
        categories = loader.get_all_categories()
        hashtags = loader.get_all_hashtags()
        
        logger.info(f"✓ Loaded {total_questions} questions from {total_files} files")
        logger.info(f"✓ Found {len(categories)} categories and {len(hashtags)} hashtags")
        
        # Test specific question retrieval
        if all_questions:
            sample_question = all_questions[0]
            question_id = sample_question['question_id']
            retrieved_question = loader.get_question_by_id(question_id)
            
            if not retrieved_question:
                logger.error("Failed to retrieve question by ID")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Question loading failed: {e}")
        return False


def test_question_selection():
    """Test spaced repetition question selection."""
    logger.info("Testing question selection algorithm...")
    
    try:
        # Test basic selection
        questions = select_quiz_questions(
            user_id=1,
            num_questions=5,
            categories=None,
            hashtags=None,
            difficulty=None
        )
        
        if not questions:
            logger.error("No questions were selected")
            return False
        
        logger.info(f"✓ Selected {len(questions)} questions for basic quiz")
        
        # Test filtered selection
        filtered_questions = select_quiz_questions(
            user_id=1,
            num_questions=3,
            categories=['algorithms'],
            difficulty='medium'
        )
        
        logger.info(f"✓ Selected {len(filtered_questions)} filtered questions")
        
        # Test selector analytics
        selector = get_spaced_repetition_selector()
        analytics = selector.get_selection_analytics(1)
        
        if 'user_profile' not in analytics:
            logger.warning("Analytics incomplete but selection working")
        else:
            logger.info("✓ Selection analytics generated successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Question selection failed: {e}")
        return False


def test_quiz_session_simulation():
    """Test a complete quiz session simulation."""
    logger.info("Testing quiz session simulation...")
    
    try:
        # Get database and select questions
        db = get_quiz_database()
        questions = select_quiz_questions(user_id=1, num_questions=3)
        
        if not questions:
            logger.error("No questions available for simulation")
            return False
        
        # Simulate answering questions
        session_stats = {'correct': 0, 'total': 0}
        
        for i, question in enumerate(questions):
            question_id = str(question['question_id'])
            question_type = question['type']
            
            # Generate a mock answer based on question type
            if question_type == 'multiple_choice':
                answer = str(question['answer'])  # Correct answer
            elif question_type == 'true_false':
                answer = str(question['answer']).lower()
            elif question_type == 'fill_blank':
                if isinstance(question['answer'], list):
                    answer = question['answer'][0]
                else:
                    answer = str(question['answer'])
            else:
                answer = "mock_answer"
            
            # Record attempt in database
            attempt_id = db.record_attempt(
                user_id=1,
                question_id=question_id,
                correct=True,  # Assume correct for simulation
                response=answer,
                latency=2.5 + i * 0.5,  # Mock latency
                hint_used=False
            )
            
            session_stats['correct'] += 1
            session_stats['total'] += 1
            
            logger.info(f"  - Question {i+1}: {question_type} -> {attempt_id}")
        
        # Get updated performance stats
        performance_stats = db.get_user_performance_stats(1)
        overall_accuracy = performance_stats.get('overall', {}).get('accuracy', 0)
        
        logger.info(f"✓ Simulation complete: {session_stats['correct']}/{session_stats['total']} correct")
        logger.info(f"✓ User overall accuracy: {overall_accuracy:.1%}")
        
        return True
        
    except Exception as e:
        logger.error(f"Quiz session simulation failed: {e}")
        return False


def test_framework_integration():
    """Test integration with Framework0 components."""
    logger.info("Testing Framework0 integration...")
    
    try:
        # Test logger integration
        test_logger = get_logger("quiz_test")
        test_logger.info("Logger integration working")
        
        # Test component lifecycle
        db = get_quiz_database()
        loader = get_question_loader()
        
        # Check if components are properly initialized
        if not db.is_initialized:
            logger.error("Database component not properly initialized")
            return False
        
        if not loader.is_initialized:
            logger.error("Question loader not properly initialized")
            return False
        
        logger.info("✓ Framework0 integration successful")
        return True
        
    except Exception as e:
        logger.error(f"Framework integration test failed: {e}")
        return False


def run_performance_benchmark():
    """Run performance benchmarks on core operations."""
    logger.info("Running performance benchmarks...")
    
    try:
        # Benchmark question loading
        start_time = time.time()
        loader = get_question_loader()
        loader.reload_questions()
        load_time = time.time() - start_time
        
        # Benchmark question selection
        start_time = time.time()
        questions = select_quiz_questions(user_id=1, num_questions=10)
        selection_time = time.time() - start_time
        
        # Benchmark database operations
        db = get_quiz_database()
        start_time = time.time()
        for i in range(5):
            stats = db.get_question_stats(f"test_question_{i}")
        db_time = time.time() - start_time
        
        logger.info(f"Performance Benchmarks:")
        logger.info(f"  - Question loading: {load_time:.3f}s")
        logger.info(f"  - Question selection: {selection_time:.3f}s") 
        logger.info(f"  - Database operations: {db_time:.3f}s")
        
        # Check if performance is acceptable
        if load_time > 5.0:
            logger.warning("Question loading is slow (>5s)")
        if selection_time > 2.0:
            logger.warning("Question selection is slow (>2s)")
        
        logger.info("✓ Performance benchmarks completed")
        return True
        
    except Exception as e:
        logger.error(f"Performance benchmark failed: {e}")
        return False


def main():
    """Run all tests and report results."""
    logger.info("=" * 60)
    logger.info("QUIZ SYSTEM TEST SUITE")
    logger.info("=" * 60)
    
    tests = [
        ("Database Initialization", test_database_initialization),
        ("Question Loading", test_question_loading),
        ("Question Selection", test_question_selection),
        ("Quiz Session Simulation", test_quiz_session_simulation),
        ("Framework Integration", test_framework_integration),
        ("Performance Benchmark", run_performance_benchmark)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Report summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{test_name:<30} {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Quiz system is ready to run.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please fix issues before running the quiz app.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)