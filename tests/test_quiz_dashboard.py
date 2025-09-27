# tests/test_quiz_dashboard.py

"""
Comprehensive test suite for Quiz Dashboard application.

This module provides thorough testing of the Quiz Dashboard components including:
- Database models and operations
- Question management and validation
- Spaced repetition algorithms
- Web application endpoints
- JSON schema validation
- User progress tracking
"""

import os
import sys
import unittest
import tempfile
import json
from unittest.mock import Mock, patch
from datetime import datetime, date, timedelta

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import components to test
from src.quiz_dashboard.models import (
    QuizDatabase, DatabaseConfig, QuestionType, DifficultyLevel,
    initialize_database
)
from src.quiz_dashboard.question_manager import (
    QuestionManager, QuestionSchemaValidator, get_question_manager
)
from src.quiz_dashboard.spaced_repetition import (
    SpacedRepetitionEngine, SM2Parameters, QuestionProgress,
    get_spaced_repetition_engine
)
from src.quiz_dashboard.web_app import create_app


class TestQuizDatabase(unittest.TestCase):
    """Test database operations and models."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        self.config = DatabaseConfig(
            database_path=self.temp_db.name,
            enable_debugging=True
        )
        self.db = QuizDatabase(self.config)
    
    def tearDown(self):
        """Clean up test database."""
        self.db.close_all_connections()
        os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test database schema creation."""
        # Verify tables exist
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        results = self.db.execute_query(tables_query)
        table_names = {row['name'] for row in results}
        
        expected_tables = {
            'users', 'questions', 'quiz_sessions', 'quiz_attempts',
            'user_progress', 'question_tags', 'performance_analytics'
        }
        
        self.assertTrue(expected_tables.issubset(table_names))
    
    def test_question_crud_operations(self):
        """Test basic question CRUD operations."""
        # Insert a test question
        insert_query = """
            INSERT INTO questions (
                question_type, title, content, question_data_json, 
                correct_answer_json, difficulty_level
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        
        question_data = {"options": [{"id": "a", "text": "Option A"}]}
        correct_answer = {"correct_answer": "a"}
        
        params = (
            QuestionType.MULTIPLE_CHOICE.value,
            "Test Question",
            "What is the answer?",
            json.dumps(question_data),
            json.dumps(correct_answer),
            3
        )
        
        rows_affected = self.db.execute_update(insert_query, params)
        self.assertEqual(rows_affected, 1)
        
        # Query the question
        select_query = "SELECT * FROM questions WHERE title = ?"
        results = self.db.execute_query(select_query, ("Test Question",))
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['question_type'], QuestionType.MULTIPLE_CHOICE.value)
        self.assertEqual(results[0]['title'], "Test Question")
    
    def test_thread_safety(self):
        """Test thread-safe database operations."""
        import threading
        
        results = []
        errors = []
        
        def insert_question(question_num):
            try:
                query = "INSERT INTO questions (question_type, title, content, question_data_json, correct_answer_json) VALUES (?, ?, ?, ?, ?)"
                params = (
                    QuestionType.TRUE_FALSE.value,
                    f"Thread Question {question_num}",
                    f"Content {question_num}",
                    "{}",
                    '{"correct_answer": true}'
                )
                rows = self.db.execute_update(query, params)
                results.append(rows)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=insert_question, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Verify results
        self.assertEqual(len(errors), 0, f"Thread errors: {errors}")
        self.assertEqual(len(results), 10)
        self.assertTrue(all(r == 1 for r in results))


class TestQuestionManager(unittest.TestCase):
    """Test question management and validation."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        self.database = initialize_database(self.temp_db.name)
        self.question_manager = QuestionManager(self.database)
        self.validator = QuestionSchemaValidator()
    
    def tearDown(self):
        """Clean up test environment."""
        self.database.close_all_connections()
        os.unlink(self.temp_db.name)
    
    def test_multiple_choice_validation(self):
        """Test multiple choice question validation."""
        valid_question = {
            "id": "test1",
            "type": "multiple_choice",
            "title": "Test Question",
            "content": "What is 2 + 2?",
            "options": [
                {"id": "a", "text": "3"},
                {"id": "b", "text": "4"},
                {"id": "c", "text": "5"}
            ],
            "correct_answer": "b",
            "difficulty": 2,
            "estimated_time": 30
        }
        
        result = self.validator.validate_question(valid_question)
        self.assertTrue(result.is_valid, f"Validation errors: {result.errors}")
        self.assertEqual(result.estimated_difficulty, 2)
    
    def test_true_false_validation(self):
        """Test true/false question validation."""
        valid_question = {
            "id": "test2",
            "type": "true_false",
            "title": "Python Statement",
            "content": "Python is a programming language.",
            "correct_answer": True,
            "difficulty": 1,
            "estimated_time": 20
        }
        
        result = self.validator.validate_question(valid_question)
        self.assertTrue(result.is_valid, f"Validation errors: {result.errors}")
    
    def test_fill_in_blank_validation(self):
        """Test fill-in-blank question validation."""
        valid_question = {
            "id": "test3",
            "type": "fill_in_blank",
            "title": "Python Function",
            "content": "The _____ function prints output to console.",
            "acceptable_answers": ["print", "print()"],
            "case_sensitive": False,
            "difficulty": 1,
            "estimated_time": 25
        }
        
        result = self.validator.validate_question(valid_question)
        self.assertTrue(result.is_valid, f"Validation errors: {result.errors}")
    
    def test_latex_detection(self):
        """Test LaTeX content detection."""
        latex_question = {
            "id": "test4",
            "type": "multiple_choice",
            "title": "Math Question",
            "content": "What is $x^2 + 2x + 1$ when $x = 3$?",
            "options": [
                {"id": "a", "text": "16"},
                {"id": "b", "text": "$3^2 + 2(3) + 1 = 16$"}
            ],
            "correct_answer": "a"
        }
        
        result = self.validator.validate_question(latex_question)
        self.assertTrue(result.latex_content)
    
    def test_question_creation(self):
        """Test question creation in database."""
        question_data = {
            "type": "multiple_choice",
            "title": "Database Test Question",
            "content": "This is a test question for database storage.",
            "options": [
                {"id": "a", "text": "Option A"},
                {"id": "b", "text": "Option B"}
            ],
            "correct_answer": "a",
            "difficulty": 3,
            "hashtags": ["test", "database"]
        }
        
        question_id = self.question_manager.create_question(question_data)
        self.assertIsNotNone(question_id)
        self.assertIsInstance(question_id, int)
        
        # Verify question can be retrieved
        retrieved_question = self.question_manager.get_question(question_id)
        self.assertIsNotNone(retrieved_question)
        self.assertEqual(retrieved_question['title'], question_data['title'])
        self.assertEqual(retrieved_question['type'], question_data['type'])
    
    def test_question_search(self):
        """Test question search functionality."""
        # Create test questions
        questions = [
            {
                "type": "multiple_choice",
                "title": "Python Question",
                "content": "About Python programming.",
                "options": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
                "correct_answer": "a",
                "hashtags": ["python", "programming"],
                "difficulty": 2
            },
            {
                "type": "true_false",
                "title": "Math Question",
                "content": "About mathematics.",
                "correct_answer": True,
                "hashtags": ["math", "algebra"],
                "difficulty": 4
            }
        ]
        
        created_ids = []
        for question in questions:
            question_id = self.question_manager.create_question(question)
            self.assertIsNotNone(question_id)
            created_ids.append(question_id)
        
        # Test search by type
        python_questions = self.question_manager.search_questions(
            question_type="multiple_choice"
        )
        self.assertGreaterEqual(len(python_questions), 1)
        
        # Test search by hashtags
        math_questions = self.question_manager.search_questions(
            hashtags=["math"]
        )
        self.assertGreaterEqual(len(math_questions), 1)
        
        # Test search by difficulty
        hard_questions = self.question_manager.search_questions(
            difficulty_range=(4, 5)
        )
        self.assertGreaterEqual(len(hard_questions), 1)


class TestSpacedRepetition(unittest.TestCase):
    """Test spaced repetition algorithms."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        self.database = initialize_database(self.temp_db.name)
        self.sr_engine = SpacedRepetitionEngine(self.database)
        
        # Create test questions
        self.question_manager = QuestionManager(self.database)
        self.test_questions = []
        
        for i in range(5):
            question_data = {
                "type": "multiple_choice",
                "title": f"Test Question {i+1}",
                "content": f"Content for question {i+1}",
                "options": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
                "correct_answer": "a",
                "difficulty": (i % 3) + 1,
                "hashtags": [f"topic{i+1}"]
            }
            question_id = self.question_manager.create_question(question_data)
            self.test_questions.append(question_id)
    
    def tearDown(self):
        """Clean up test environment."""
        self.database.close_all_connections()
        os.unlink(self.temp_db.name)
    
    def test_sm2_algorithm_correct_answer(self):
        """Test SM-2 algorithm with correct answer."""
        user_id = 1
        question_id = self.test_questions[0]
        
        # Process correct answer
        progress = self.sr_engine.process_question_attempt(
            user_id=user_id,
            question_id=question_id,
            performance_score=4.0,  # Good performance
            time_taken_seconds=30.0,
            is_correct=True
        )
        
        self.assertEqual(progress.user_id, user_id)
        self.assertEqual(progress.question_id, question_id)
        self.assertEqual(progress.total_attempts, 1)
        self.assertEqual(progress.correct_attempts, 1)
        self.assertGreater(progress.easiness_factor, 2.0)
        self.assertIsNotNone(progress.next_review_date)
    
    def test_sm2_algorithm_incorrect_answer(self):
        """Test SM-2 algorithm with incorrect answer."""
        user_id = 1
        question_id = self.test_questions[1]
        
        # Process incorrect answer
        progress = self.sr_engine.process_question_attempt(
            user_id=user_id,
            question_id=question_id,
            performance_score=1.0,  # Poor performance
            time_taken_seconds=60.0,
            is_correct=False
        )
        
        self.assertEqual(progress.total_attempts, 1)
        self.assertEqual(progress.correct_attempts, 0)
        self.assertEqual(progress.repetition_count, 0)  # Reset on failure
        self.assertEqual(progress.interval_days, 1)  # Back to beginning
    
    def test_question_selection(self):
        """Test intelligent question selection."""
        user_id = 1
        
        # Create some progress data by answering questions
        for i, question_id in enumerate(self.test_questions[:3]):
            self.sr_engine.process_question_attempt(
                user_id=user_id,
                question_id=question_id,
                performance_score=3.0 + i,
                time_taken_seconds=30.0,
                is_correct=True
            )
        
        # Select next questions
        selected_questions = self.sr_engine.select_next_questions(
            user_id=user_id,
            count=3
        )
        
        self.assertIsInstance(selected_questions, list)
        self.assertGreater(len(selected_questions), 0)
        self.assertLessEqual(len(selected_questions), 3)
        
        # Verify questions are valid IDs
        for question_id in selected_questions:
            self.assertIsInstance(question_id, int)
            self.assertIn(question_id, self.test_questions)
    
    def test_mastery_calculation(self):
        """Test mastery level calculation."""
        user_id = 1
        question_id = self.test_questions[0]
        
        # Simulate multiple attempts with improving performance
        performance_scores = [2.0, 3.0, 4.0, 4.5, 5.0]
        
        for score in performance_scores:
            progress = self.sr_engine.process_question_attempt(
                user_id=user_id,
                question_id=question_id,
                performance_score=score,
                time_taken_seconds=30.0,
                is_correct=score >= 3.0
            )
        
        # Mastery should improve over time
        self.assertGreater(progress.mastery_level, 50.0)
        self.assertGreater(progress.repetition_count, 2)
    
    def test_user_statistics(self):
        """Test user statistics generation."""
        user_id = 1
        
        # Create progress for multiple questions
        for question_id in self.test_questions:
            self.sr_engine.process_question_attempt(
                user_id=user_id,
                question_id=question_id,
                performance_score=4.0,
                time_taken_seconds=35.0,
                is_correct=True
            )
        
        # Get user statistics
        stats = self.sr_engine.get_user_statistics(user_id)
        
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['user_id'], user_id)
        self.assertEqual(stats['total_questions_attempted'], len(self.test_questions))
        self.assertGreater(stats['average_mastery'], 0)
        self.assertIn('difficulty_distribution', stats)


class TestWebApplication(unittest.TestCase):
    """Test Flask web application."""
    
    def setUp(self):
        """Set up test Flask app."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        self.app = create_app(database_path=self.temp_db.name)
        self.app.config['TESTING'] = True
        self.client = self.app.app.test_client()
        
        # Create test question
        with self.app.app.app_context():
            question_manager = get_question_manager()
            self.test_question_id = question_manager.create_question({
                "type": "multiple_choice",
                "title": "Test Web Question",
                "content": "Test content",
                "options": [
                    {"id": "a", "text": "Option A"},
                    {"id": "b", "text": "Option B"}
                ],
                "correct_answer": "a",
                "difficulty": 2
            })
    
    def tearDown(self):
        """Clean up test environment."""
        os.unlink(self.temp_db.name)
    
    def test_index_page(self):
        """Test index page loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quiz Dashboard', response.data)
    
    def test_dashboard_page(self):
        """Test dashboard page loads."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Choose Your Role', response.data)
    
    def test_student_dashboard(self):
        """Test student dashboard loads."""
        response = self.client.get('/student')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)
    
    def test_instructor_dashboard(self):
        """Test instructor dashboard loads."""
        response = self.client.get('/instructor')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Instructor Dashboard', response.data)
    
    def test_quiz_session_creation(self):
        """Test quiz session creation."""
        response = self.client.post('/quiz/start', data={
            'question_count': '5',
            'difficulty_level': '2',
            'spaced_repetition': 'on'
        }, follow_redirects=False)
        
        # Should redirect to quiz interface
        self.assertEqual(response.status_code, 302)
        self.assertIn('/quiz/', response.location)
    
    def test_api_question_search(self):
        """Test API question search endpoint."""
        response = self.client.get('/api/questions/search?limit=5')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('questions', data)
        self.assertIn('total', data)
        self.assertIsInstance(data['questions'], list)
    
    def test_api_question_validation(self):
        """Test API question validation endpoint."""
        valid_question = {
            "type": "true_false",
            "title": "API Test Question",
            "content": "This is a test.",
            "correct_answer": True
        }
        
        response = self.client.post('/api/questions/validate',
                                  json=valid_question,
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('is_valid', data)
    
    def test_404_error_handling(self):
        """Test 404 error handling."""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        # Initialize components
        self.database = initialize_database(self.temp_db.name)
        self.question_manager = get_question_manager(self.database)
        self.sr_engine = get_spaced_repetition_engine(self.database)
        
    def tearDown(self):
        """Clean up integration test environment."""
        self.database.close_all_connections()
        os.unlink(self.temp_db.name)
    
    def test_complete_learning_workflow(self):
        """Test complete learning workflow from question creation to analysis."""
        
        # Step 1: Create questions
        questions_data = [
            {
                "type": "multiple_choice",
                "title": "Integration Test Question 1",
                "content": "What is the capital of France?",
                "options": [
                    {"id": "a", "text": "London"},
                    {"id": "b", "text": "Paris"},
                    {"id": "c", "text": "Berlin"}
                ],
                "correct_answer": "b",
                "difficulty": 2,
                "hashtags": ["geography", "europe"]
            },
            {
                "type": "true_false",
                "title": "Integration Test Question 2",
                "content": "Python is a programming language.",
                "correct_answer": True,
                "difficulty": 1,
                "hashtags": ["python", "programming"]
            }
        ]
        
        created_questions = []
        for question_data in questions_data:
            question_id = self.question_manager.create_question(question_data)
            self.assertIsNotNone(question_id)
            created_questions.append(question_id)
        
        # Step 2: Simulate user taking quiz
        user_id = 1
        
        for question_id in created_questions:
            # Get question
            question = self.question_manager.get_question(question_id)
            self.assertIsNotNone(question)
            
            # Simulate correct answer
            progress = self.sr_engine.process_question_attempt(
                user_id=user_id,
                question_id=question_id,
                performance_score=4.0,
                time_taken_seconds=30.0,
                is_correct=True
            )
            
            self.assertIsNotNone(progress)
            self.assertEqual(progress.user_id, user_id)
            self.assertEqual(progress.question_id, question_id)
        
        # Step 3: Get recommendations
        recommendations = self.sr_engine.select_next_questions(
            user_id=user_id,
            count=5
        )
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Step 4: Get user statistics
        stats = self.sr_engine.get_user_statistics(user_id)
        
        self.assertEqual(stats['user_id'], user_id)
        self.assertEqual(stats['total_questions_attempted'], len(created_questions))
        self.assertGreater(stats['average_mastery'], 0)
        
        # Step 5: Search questions
        search_results = self.question_manager.search_questions(
            hashtags=["programming"],
            limit=10
        )
        
        self.assertIsInstance(search_results, list)
        # Should find at least the programming question
        programming_questions = [q for q in search_results if "programming" in q.get('hashtags', [])]
        self.assertGreater(len(programming_questions), 0)


def run_tests():
    """Run all test suites."""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        TestQuizDatabase,
        TestQuestionManager, 
        TestSpacedRepetition,
        TestWebApplication,
        TestIntegration
    ]
    
    for test_case in test_cases:
        tests = loader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)