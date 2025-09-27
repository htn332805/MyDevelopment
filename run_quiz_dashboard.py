#!/usr/bin/env python3
# run_quiz_dashboard.py

"""
Quiz Dashboard Application Runner.

This script provides a simple way to run the Quiz Dashboard web application
with proper initialization of the database and sample data.

Usage:
    python run_quiz_dashboard.py [--host HOST] [--port PORT] [--debug]
    
Example:
    python run_quiz_dashboard.py --host 0.0.0.0 --port 5000 --debug
"""

import os
import sys
import argparse
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import Framework0 components
from src.core.logger import get_logger
from src.quiz_dashboard.web_app import create_app
from src.quiz_dashboard.models import initialize_database
from src.quiz_dashboard.question_manager import get_question_manager

# Initialize logger
logger = get_logger(__name__)


def create_sample_questions() -> Any:
    """Create sample questions for demonstration."""
    
    sample_questions = [
        {
            "id": "q1",
            "type": "multiple_choice",
            "title": "Basic Python Syntax",
            "content": "What is the correct way to create a list in Python?",
            "explanation": "Lists in Python are created using square brackets [].",
            "difficulty": 2,
            "estimated_time": 30,
            "hashtags": ["python", "basics", "syntax"],
            "options": [
                {"id": "a", "text": "list = []"},
                {"id": "b", "text": "list = {}"},
                {"id": "c", "text": "list = ()"},
                {"id": "d", "text": "list = ||"}
            ],
            "correct_answer": "a",
            "shuffle_options": True
        },
        {
            "id": "q2", 
            "type": "true_false",
            "title": "Python is Case Sensitive",
            "content": "Python is a case-sensitive programming language.",
            "explanation": "Yes, Python is case-sensitive. Variable names 'var' and 'Var' are different.",
            "difficulty": 1,
            "estimated_time": 20,
            "hashtags": ["python", "basics"],
            "correct_answer": True
        },
        {
            "id": "q3",
            "type": "fill_in_blank",
            "title": "Python Print Function",
            "content": "Complete the code to print 'Hello World': _____(\"Hello World\")",
            "explanation": "The print() function is used to output text in Python.",
            "difficulty": 1,
            "estimated_time": 25,
            "hashtags": ["python", "basics", "print"],
            "acceptable_answers": ["print", "print()", "Print"],
            "case_sensitive": False
        },
        {
            "id": "q4",
            "type": "multiple_choice", 
            "title": "Mathematical Expression",
            "content": "What is the result of $2^3 + \\sqrt{16}$ ?",
            "explanation": "Calculate: $2^3 = 8$ and $\\sqrt{16} = 4$, so $8 + 4 = 12$.",
            "difficulty": 3,
            "estimated_time": 45,
            "hashtags": ["math", "algebra", "exponents"],
            "options": [
                {"id": "a", "text": "10"},
                {"id": "b", "text": "12"},
                {"id": "c", "text": "14"},
                {"id": "d", "text": "16"}
            ],
            "correct_answer": "b",
            "shuffle_options": True
        },
        {
            "id": "q5",
            "type": "reorder_sequence",
            "title": "Software Development Process",
            "content": "Arrange the following steps of software development in the correct order:",
            "explanation": "The typical software development process follows: Requirements → Design → Implementation → Testing → Deployment.",
            "difficulty": 3,
            "estimated_time": 60,
            "hashtags": ["software", "process", "development"],
            "items": [
                {"id": "req", "text": "Requirements Gathering"},
                {"id": "design", "text": "System Design"},
                {"id": "impl", "text": "Implementation"},
                {"id": "test", "text": "Testing"},
                {"id": "deploy", "text": "Deployment"}
            ],
            "correct_order": ["req", "design", "impl", "test", "deploy"],
            "partial_credit": True
        },
        {
            "id": "q6",
            "type": "matching_pairs",
            "title": "Programming Languages and Their Creators",
            "content": "Match each programming language with its creator:",
            "explanation": "These are the original creators or key figures in developing these languages.",
            "difficulty": 4,
            "estimated_time": 90,
            "hashtags": ["programming", "history", "languages"],
            "left_items": [
                {"id": "python", "text": "Python"},
                {"id": "java", "text": "Java"},
                {"id": "cpp", "text": "C++"}
            ],
            "right_items": [
                {"id": "guido", "text": "Guido van Rossum"},
                {"id": "james", "text": "James Gosling"},
                {"id": "bjarne", "text": "Bjarne Stroustrup"}
            ],
            "correct_matches": [
                {"left_id": "python", "right_id": "guido"},
                {"left_id": "java", "right_id": "james"},
                {"left_id": "cpp", "right_id": "bjarne"}
            ],
            "allow_multiple_matches": False
        }
    ]
    
    return sample_questions


def initialize_sample_data() -> Any:
    """Initialize database with sample questions."""
    
    try:
        logger.info("Initializing sample data...")
        
        # Get question manager
        question_manager = get_question_manager()
        
        # Create sample questions
        sample_questions = create_sample_questions()
        
        # Check if questions already exist
        existing_questions = question_manager.search_questions(limit=1)
        if existing_questions:
            logger.info("Sample questions already exist, skipping initialization")
            return
        
        # Import sample questions
        created_count = 0
        for question_data in sample_questions:
            try:
                question_id = question_manager.create_question(question_data, created_by=1)
                if question_id:
                    created_count += 1
                    logger.debug(f"Created sample question: {question_data['title']}")
                else:
                    logger.warning(f"Failed to create question: {question_data['title']}")
            except Exception as e:
                logger.error(f"Error creating question {question_data['title']}: {e}")
        
        logger.info(f"Sample data initialization complete: {created_count} questions created")
        
    except Exception as e:
        logger.error(f"Failed to initialize sample data: {e}")


def main() -> Any:
    """Main application entry point."""
    
    parser = argparse.ArgumentParser(description="Quiz Dashboard Application")
    parser.add_argument("--host", default="127.0.0.1", help="Host address to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--database", default="quiz_dashboard.db", help="Database file path")
    parser.add_argument("--init-sample-data", action="store_true", help="Initialize with sample questions")
    
    args = parser.parse_args()
    
    try:
        # Initialize database
        logger.info(f"Initializing Quiz Dashboard database: {args.database}")
        initialize_database(args.database)
        
        # Initialize sample data if requested
        if args.init_sample_data or not os.path.exists(args.database):
            initialize_sample_data()
        
        # Create Flask app
        logger.info("Creating Quiz Dashboard web application...")
        app = create_app(database_path=args.database)
        
        # Display startup information
        print("\n" + "="*60)
        print("🎓 Quiz Dashboard - Interactive Learning Platform")
        print("="*60)
        print(f"🌐 Server: http://{args.host}:{args.port}")
        print(f"📊 Database: {args.database}")
        print(f"🐛 Debug Mode: {'Enabled' if args.debug else 'Disabled'}")
        print("="*60)
        print("\nFeatures:")
        print("  • Spaced Repetition (SM-2) Algorithm")
        print("  • Multi-type Questions (MC, T/F, Fill-in, Reorder, Matching)")
        print("  • Adaptive Difficulty & Anti-clustering")
        print("  • LaTeX Math Support with MathJax")
        print("  • Performance Analytics & Progress Tracking")
        print("  • Responsive Bootstrap UI")
        print("\nPress Ctrl+C to stop the server")
        print("="*60 + "\n")
        
        # Start the application
        app.run(host=args.host, port=args.port, debug=args.debug)
        
    except KeyboardInterrupt:
        logger.info("Quiz Dashboard server stopped by user")
        print("\nQuiz Dashboard server stopped. Thank you for using our platform!")
    except Exception as e:
        logger.error(f"Failed to start Quiz Dashboard: {e}")
        print(f"\nError starting Quiz Dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()