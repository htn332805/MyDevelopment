# src/quiz_dashboard/__init__.py

"""
Interactive Quiz Dashboard Application for Framework0.

This module provides a complete quiz system with advanced pedagogical algorithms,
multi-type question support, and comprehensive analytics. Built on Framework0's
enhanced architecture with robust error handling and monitoring.

Features:
- Multi-type questions (Multiple Choice, True/False, Fill-in-Blank, Reorder, Matching)
- Spaced Repetition (SM-2) algorithm for optimal learning
- Adaptive difficulty adjustment based on performance
- Anti-clustering to prevent similar questions appearing consecutively
- Comprehensive user analytics and progress tracking
- MathJax integration for LaTeX mathematical notation
- Responsive Bootstrap UI with mobile support
- Thread-safe SQLite database operations
- JSON schema validation for question formats
"""

from typing import Dict, Any, List, Optional

# Import core components
from src.core.logger import get_logger

# Initialize module logger
logger = get_logger(__name__)

# Version information
__version__ = "1.0.0"
__author__ = "Framework0 Development Team"

# Module constants
SUPPORTED_QUESTION_TYPES = [
    "multiple_choice",
    "true_false", 
    "fill_in_blank",
    "reorder_sequence",
    "matching_pairs"
]

DEFAULT_DATABASE_PATH = "quiz_dashboard.db"
DEFAULT_QUESTIONS_PATH = "quiz_questions.json"

logger.info(f"Quiz Dashboard module initialized (version {__version__})")