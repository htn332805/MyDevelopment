# quiz-app/utils/qloader.py

"""
Question loader and validation system for quiz application.

This module provides comprehensive question management including:
- JSON question file loading and validation
- Question schema validation with detailed error reporting
- Question pool management and caching
- Multi-format support (JSON, CSV import)
- Real-time question validation and hot-reload
- Question metadata extraction and indexing

Integrates with Framework0's validation and caching systems.
"""

import json
import csv
import glob
import os
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union, Tuple, Set
from pathlib import Path
from dataclasses import dataclass, field, asdict
import threading
import uuid
import re

# Import Framework0 components
from src.core.logger import get_logger
from src.core.interfaces import ComponentLifecycle, Configurable
from src.core.decorators_v2 import monitor_resources, debug_trace
from src.core.error_handling import handle_errors, ErrorCategory

# Import jsonschema for validation
import jsonschema
from jsonschema import validate, ValidationError

# Import quiz database
sys.path.append("..")  # Add parent directory for imports
from models.storage import get_quiz_database, QuizDatabase

# Initialize logger with debug support
logger = get_logger(__name__, debug=True)


@dataclass
class QuestionValidationResult:
    """Result of question validation with detailed feedback."""
    valid: bool  # Whether question passed validation
    question_id: str  # Question identifier
    errors: List[str] = field(default_factory=list)  # Validation errors
    warnings: List[str] = field(default_factory=list)  # Non-critical warnings
    question_type: Optional[str] = None  # Validated question type
    categories: List[str] = field(default_factory=list)  # Question categories
    hashtags: List[str] = field(default_factory=list)  # Question hashtags


@dataclass
class QuestionPool:
    """Container for loaded and validated questions."""
    questions: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # All questions
    by_category: Dict[str, List[str]] = field(default_factory=dict)  # Questions by category
    by_hashtag: Dict[str, List[str]] = field(default_factory=dict)  # Questions by hashtag
    by_type: Dict[str, List[str]] = field(default_factory=dict)  # Questions by type
    by_difficulty: Dict[str, List[str]] = field(default_factory=dict)  # Questions by difficulty
    metadata: Dict[str, Any] = field(default_factory=dict)  # Pool metadata
    last_updated: Optional[datetime] = None  # Last update timestamp


class QuestionLoader(ComponentLifecycle, Configurable):
    """
    Comprehensive question loader with validation and caching.
    
    Provides centralized question management with real-time validation,
    smart caching, and integration with the quiz database system.
    """
    
    def __init__(self, questions_dir: str = "quiz-app/data/questions",
                 schema_path: str = "quiz-app/schemas/question_schema.json"):
        """Initialize question loader with directories and schema."""
        super().__init__()
        self.questions_dir = Path(questions_dir)  # Questions directory path
        self.schema_path = Path(schema_path)  # JSON schema file path
        self.question_pool = QuestionPool()  # In-memory question pool
        self.schema = None  # Loaded JSON schema for validation
        self.db = None  # Quiz database instance
        self.file_watchers = {}  # File modification time tracking
        self.load_lock = threading.Lock()  # Thread safety for loading
        self.validation_stats = {  # Validation statistics
            'total_loaded': 0,
            'total_valid': 0,
            'total_errors': 0,
            'last_load_time': None
        }
        
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Initialize question loader with configuration."""
        logger.info(f"Initializing question loader from {self.questions_dir}")
        
        # Create questions directory if it doesn't exist
        self.questions_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and validate JSON schema
        self._load_schema()
        
        # Initialize database connection
        self.db = get_quiz_database()
        
        # Load all question files
        self.reload_questions()
        
        logger.info(f"Question loader initialized with {len(self.question_pool.questions)} questions")
        
    def _do_cleanup(self) -> None:
        """Clean up question loader resources."""
        logger.info("Cleaning up question loader")
        
        # Clear question pool
        self.question_pool = QuestionPool()
        
        # Clear file watchers
        self.file_watchers.clear()
        
        logger.info("Question loader cleanup completed")
    
    @monitor_resources
    def _load_schema(self) -> None:
        """Load and validate JSON schema for questions."""
        try:
            # Load schema file
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
            
            # Validate schema itself
            jsonschema.Draft7Validator.check_schema(self.schema)
            
            logger.debug(f"Loaded question schema from {self.schema_path}")
            
        except FileNotFoundError:
            logger.error(f"Question schema not found at {self.schema_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in schema file: {e}")
            raise
        except jsonschema.SchemaError as e:
            logger.error(f"Invalid JSON schema: {e}")
            raise
    
    @monitor_resources
    @debug_trace
    def reload_questions(self) -> Tuple[int, int, List[str]]:
        """Reload all questions from files with validation."""
        with self.load_lock:  # Thread-safe loading
            logger.info("Reloading all question files")
            
            # Clear existing question pool
            self.question_pool = QuestionPool()
            
            # Track loading statistics
            total_files = 0
            total_questions = 0
            errors = []
            
            # Find all JSON question files
            question_files = list(self.questions_dir.glob("*.json"))
            
            for file_path in question_files:
                try:
                    # Load and validate file
                    file_questions, file_errors = self._load_question_file(file_path)
                    
                    total_files += 1
                    total_questions += len(file_questions)
                    errors.extend(file_errors)
                    
                    # Update file modification time
                    self.file_watchers[str(file_path)] = file_path.stat().st_mtime
                    
                except Exception as e:
                    error_msg = f"Failed to load {file_path}: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            
            # Build question indexes
            self._build_question_indexes()
            
            # Update metadata
            self.question_pool.metadata = {
                'total_files': total_files,
                'total_questions': total_questions,
                'total_errors': len(errors),
                'load_timestamp': datetime.now(timezone.utc).isoformat()
            }
            self.question_pool.last_updated = datetime.now(timezone.utc)
            
            # Update validation statistics
            self.validation_stats.update({
                'total_loaded': total_questions,
                'total_valid': total_questions - len(errors),
                'total_errors': len(errors),
                'last_load_time': datetime.now(timezone.utc).isoformat()
            })
            
            logger.info(f"Loaded {total_questions} questions from {total_files} files with {len(errors)} errors")
            return total_files, total_questions, errors
    
    def _load_question_file(self, file_path: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Load and validate questions from a single JSON file."""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse JSON content
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                return [], [f"Invalid JSON in {file_path}: {e}"]
            
            # Handle both single question and array formats
            questions_data = data if isinstance(data, list) else [data]
            
            # Validate each question
            valid_questions = []
            errors = []
            
            for i, question_data in enumerate(questions_data):
                try:
                    # Validate question with schema
                    validation_result = self.validate_question(question_data)
                    
                    if validation_result.valid:
                        # Add file metadata
                        question_data['_source_file'] = str(file_path)
                        question_data['_file_index'] = i
                        
                        # Add to question pool
                        question_id = str(question_data['question_id'])
                        self.question_pool.questions[question_id] = question_data
                        
                        # Store metadata in database
                        if self.db:
                            self.db.store_question_metadata(question_data)
                        
                        valid_questions.append(question_data)
                        
                    else:
                        # Collect validation errors
                        error_prefix = f"{file_path}[{i}]"
                        for error in validation_result.errors:
                            errors.append(f"{error_prefix}: {error}")
                        
                except Exception as e:
                    errors.append(f"{file_path}[{i}]: Validation failed: {e}")
            
            logger.debug(f"Loaded {len(valid_questions)} valid questions from {file_path}")
            return valid_questions, errors
            
        except Exception as e:
            return [], [f"Failed to read {file_path}: {e}"]
    
    def validate_question(self, question_data: Dict[str, Any]) -> QuestionValidationResult:
        """Validate a single question against the schema and business rules."""
        question_id = str(question_data.get('question_id', 'unknown'))
        result = QuestionValidationResult(
            valid=True,
            question_id=question_id,
            question_type=question_data.get('type')
        )
        
        try:
            # Schema validation
            validate(instance=question_data, schema=self.schema)
            
            # Additional business rule validation
            self._validate_business_rules(question_data, result)
            
            # Extract categories and hashtags
            result.categories = question_data.get('categories', [])
            result.hashtags = question_data.get('hashtags', [])
            
            logger.debug(f"Question {question_id} validation: {len(result.errors)} errors, {len(result.warnings)} warnings")
            
        except ValidationError as e:
            result.valid = False
            result.errors.append(f"Schema validation failed: {e.message}")
            logger.debug(f"Question {question_id} failed schema validation: {e.message}")
        except Exception as e:
            result.valid = False
            result.errors.append(f"Validation error: {e}")
            logger.error(f"Unexpected validation error for question {question_id}: {e}")
        
        # Mark invalid if any errors
        if result.errors:
            result.valid = False
        
        return result
    
    def _validate_business_rules(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        """Apply additional business rule validation beyond schema."""
        question_type = question_data.get('type')
        
        # Type-specific validation
        if question_type == 'multiple_choice':
            self._validate_multiple_choice(question_data, result)
        elif question_type == 'true_false':
            self._validate_true_false(question_data, result)
        elif question_type == 'fill_blank':
            self._validate_fill_blank(question_data, result)
        elif question_type == 'reorder':
            self._validate_reorder(question_data, result)
        elif question_type == 'matching':
            self._validate_matching(question_data, result)
        
        # Common validation rules
        self._validate_common_rules(question_data, result)
    
    def _validate_multiple_choice(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        """Validate multiple choice specific rules."""
        choices = question_data.get('choices', [])
        answer = question_data.get('answer')
        
        # Check minimum choices
        if len(choices) < 2:
            result.errors.append("Multiple choice questions must have at least 2 choices")
        
        # Check answer index validity
        if not isinstance(answer, int) or answer < 0 or answer >= len(choices):
            result.errors.append(f"Answer index {answer} is invalid for {len(choices)} choices")
        
        # Check for duplicate choices
        if len(choices) != len(set(choices)):
            result.warnings.append("Duplicate choices detected")
        
        # Recommend minimum 4 choices for good questions
        if len(choices) < 4:
            result.warnings.append("Consider adding more choices for better question quality")
    
    def _validate_true_false(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        """Validate true/false specific rules."""
        answer = question_data.get('answer')
        
        # Check answer is boolean
        if not isinstance(answer, bool):
            result.errors.append("True/false questions must have boolean answer")
    
    def _validate_fill_blank(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        """Validate fill-in-the-blank specific rules."""
        answer = question_data.get('answer')
        prompt = question_data.get('prompt', '')
        
        # Check for blank placeholder in prompt
        if '____' not in prompt and '_____' not in prompt:
            result.warnings.append("Consider using ____ to clearly indicate the blank")
        
        # Validate answer format
        if isinstance(answer, str):
            if not answer.strip():
                result.errors.append("Fill-in-the-blank answer cannot be empty")
        elif isinstance(answer, list):
            if not answer or not all(isinstance(a, str) and a.strip() for a in answer):
                result.errors.append("Fill-in-the-blank answer list cannot be empty or contain empty strings")
        else:
            result.errors.append("Fill-in-the-blank answer must be string or list of strings")
    
    def _validate_reorder(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        """Validate reorder/sequence specific rules."""
        reorder = question_data.get('reorder', [])
        
        # Check minimum items
        if len(reorder) < 2:
            result.errors.append("Reorder questions must have at least 2 items")
        
        # Check for duplicates
        if len(reorder) != len(set(reorder)):
            result.errors.append("Reorder questions cannot have duplicate items")
        
        # Recommend reasonable limits
        if len(reorder) > 10:
            result.warnings.append("Consider limiting reorder questions to 10 or fewer items")
    
    def _validate_matching(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        """Validate matching question specific rules."""
        matching = question_data.get('matching', {})
        left = matching.get('left', [])
        right = matching.get('right', [])
        pairs = matching.get('pairs', [])
        
        # Check minimum items
        if len(left) < 2 or len(right) < 2:
            result.errors.append("Matching questions must have at least 2 items on each side")
        
        # Check pairs validity
        for i, pair in enumerate(pairs):
            if len(pair) != 2:
                result.errors.append(f"Matching pair {i} must have exactly 2 elements")
                continue
            
            left_idx, right_idx = pair
            if left_idx < 0 or left_idx >= len(left):
                result.errors.append(f"Left index {left_idx} in pair {i} is out of range")
            if right_idx < 0 or right_idx >= len(right):
                result.errors.append(f"Right index {right_idx} in pair {i} is out of range")
        
        # Check all items are paired
        if len(pairs) != len(left):
            result.warnings.append("Not all left items are paired - some may be distractors")
    
    def _validate_common_rules(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        """Validate common rules across all question types."""
        prompt = question_data.get('prompt', '')
        
        # Check prompt length
        if len(prompt.strip()) < 10:
            result.warnings.append("Question prompt is very short - consider adding more detail")
        elif len(prompt) > 1000:
            result.warnings.append("Question prompt is very long - consider simplifying")
        
        # Check for LaTeX syntax
        if '$$' in prompt or '\\(' in prompt or '\\[' in prompt:
            result.warnings.append("LaTeX detected - ensure MathJax is configured for rendering")
        
        # Validate hashtags format
        hashtags = question_data.get('hashtags', [])
        for hashtag in hashtags:
            if not hashtag.startswith('#'):
                result.warnings.append(f"Hashtag '{hashtag}' should start with #")
        
        # Check for created_at timestamp
        if 'created_at' not in question_data:
            question_data['created_at'] = datetime.now(timezone.utc).isoformat()
        
        # Generate question_id if missing
        if 'question_id' not in question_data:
            question_data['question_id'] = str(uuid.uuid4())
    
    def _build_question_indexes(self) -> None:
        """Build indexes for efficient question lookup."""
        logger.debug("Building question indexes")
        
        # Clear existing indexes
        self.question_pool.by_category.clear()
        self.question_pool.by_hashtag.clear()
        self.question_pool.by_type.clear()
        self.question_pool.by_difficulty.clear()
        
        # Build indexes from loaded questions
        for question_id, question_data in self.question_pool.questions.items():
            # Index by categories
            categories = question_data.get('categories', [])
            for category in categories:
                if category not in self.question_pool.by_category:
                    self.question_pool.by_category[category] = []
                self.question_pool.by_category[category].append(question_id)
            
            # Index by hashtags
            hashtags = question_data.get('hashtags', [])
            for hashtag in hashtags:
                if hashtag not in self.question_pool.by_hashtag:
                    self.question_pool.by_hashtag[hashtag] = []
                self.question_pool.by_hashtag[hashtag].append(question_id)
            
            # Index by type
            question_type = question_data.get('type')
            if question_type:
                if question_type not in self.question_pool.by_type:
                    self.question_pool.by_type[question_type] = []
                self.question_pool.by_type[question_type].append(question_id)
            
            # Index by difficulty
            difficulty = question_data.get('difficulty', 'medium')
            if difficulty not in self.question_pool.by_difficulty:
                self.question_pool.by_difficulty[difficulty] = []
            self.question_pool.by_difficulty[difficulty].append(question_id)
        
        logger.debug(f"Built indexes: {len(self.question_pool.by_category)} categories, "
                    f"{len(self.question_pool.by_hashtag)} hashtags, "
                    f"{len(self.question_pool.by_type)} types, "
                    f"{len(self.question_pool.by_difficulty)} difficulties")
    
    @monitor_resources
    def get_questions_by_criteria(self, categories: Optional[List[str]] = None,
                                hashtags: Optional[List[str]] = None,
                                question_type: Optional[str] = None,
                                difficulty: Optional[str] = None,
                                limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get questions matching specified criteria."""
        logger.debug(f"Filtering questions by criteria: categories={categories}, "
                    f"hashtags={hashtags}, type={question_type}, difficulty={difficulty}")
        
        # Start with all question IDs
        candidate_ids = set(self.question_pool.questions.keys())
        
        # Apply category filter
        if categories:
            category_ids = set()
            for category in categories:
                category_ids.update(self.question_pool.by_category.get(category, []))
            candidate_ids &= category_ids
        
        # Apply hashtag filter
        if hashtags:
            hashtag_ids = set()
            for hashtag in hashtags:
                hashtag_ids.update(self.question_pool.by_hashtag.get(hashtag, []))
            candidate_ids &= hashtag_ids
        
        # Apply type filter
        if question_type:
            type_ids = set(self.question_pool.by_type.get(question_type, []))
            candidate_ids &= type_ids
        
        # Apply difficulty filter
        if difficulty:
            difficulty_ids = set(self.question_pool.by_difficulty.get(difficulty, []))
            candidate_ids &= difficulty_ids
        
        # Get question objects
        questions = []
        for question_id in candidate_ids:
            questions.append(self.question_pool.questions[question_id])
        
        # Apply limit
        if limit and len(questions) > limit:
            questions = questions[:limit]
        
        logger.debug(f"Filtered to {len(questions)} questions")
        return questions
    
    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific question by ID."""
        return self.question_pool.questions.get(str(question_id))
    
    def get_all_categories(self) -> List[str]:
        """Get list of all available categories."""
        return list(self.question_pool.by_category.keys())
    
    def get_all_hashtags(self) -> List[str]:
        """Get list of all available hashtags."""
        return list(self.question_pool.by_hashtag.keys())
    
    def get_question_types(self) -> List[str]:
        """Get list of all question types."""
        return list(self.question_pool.by_type.keys())
    
    def get_pool_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the question pool."""
        return {
            'total_questions': len(self.question_pool.questions),
            'by_type': {qtype: len(questions) for qtype, questions in self.question_pool.by_type.items()},
            'by_difficulty': {diff: len(questions) for diff, questions in self.question_pool.by_difficulty.items()},
            'by_category': {cat: len(questions) for cat, questions in self.question_pool.by_category.items()},
            'total_categories': len(self.question_pool.by_category),
            'total_hashtags': len(self.question_pool.by_hashtag),
            'last_updated': self.question_pool.last_updated.isoformat() if self.question_pool.last_updated else None,
            'validation_stats': self.validation_stats.copy(),
            'metadata': self.question_pool.metadata.copy()
        }
    
    @monitor_resources
    def import_from_csv(self, csv_path: str, type_column: str = 'type',
                       prompt_column: str = 'prompt', 
                       answer_column: str = 'answer') -> Tuple[int, List[str]]:
        """Import questions from CSV file with automatic type conversion."""
        try:
            logger.info(f"Importing questions from CSV: {csv_path}")
            
            questions = []
            errors = []
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader):
                    try:
                        # Build basic question structure
                        question = {
                            'question_id': row.get('question_id', str(uuid.uuid4())),
                            'type': row.get(type_column, 'multiple_choice'),
                            'prompt': row.get(prompt_column, ''),
                            'created_at': datetime.now(timezone.utc).isoformat(),
                            'created_by': 'csv_import'
                        }
                        
                        # Handle answer based on type
                        answer_text = row.get(answer_column, '')
                        if question['type'] == 'true_false':
                            question['answer'] = answer_text.lower() in ['true', '1', 'yes']
                        elif question['type'] == 'multiple_choice' and 'choices' in row:
                            choices = row['choices'].split('|') if row['choices'] else []
                            question['choices'] = choices
                            try:
                                question['answer'] = int(answer_text)
                            except ValueError:
                                question['answer'] = choices.index(answer_text) if answer_text in choices else 0
                        else:
                            question['answer'] = answer_text
                        
                        # Add optional fields
                        for field in ['difficulty', 'hint', 'explanation', 'categories', 'hashtags']:
                            if field in row and row[field]:
                                if field in ['categories', 'hashtags']:
                                    question[field] = [item.strip() for item in row[field].split('|')]
                                else:
                                    question[field] = row[field]
                        
                        # Validate question
                        validation_result = self.validate_question(question)
                        if validation_result.valid:
                            questions.append(question)
                        else:
                            errors.extend([f"Row {i+1}: {error}" for error in validation_result.errors])
                        
                    except Exception as e:
                        errors.append(f"Row {i+1}: {e}")
            
            # Save valid questions to JSON file
            if questions:
                output_file = self.questions_dir / f"imported_{int(time.time())}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(questions, f, indent=2, ensure_ascii=False)
                
                # Reload questions to include imports
                self.reload_questions()
            
            logger.info(f"Imported {len(questions)} questions from CSV with {len(errors)} errors")
            return len(questions), errors
            
        except Exception as e:
            logger.error(f"Failed to import CSV: {e}")
            return 0, [f"CSV import failed: {e}"]


# Global question loader instance
_question_loader: Optional[QuestionLoader] = None
_loader_lock = threading.Lock()


def get_question_loader(questions_dir: str = "quiz-app/data/questions",
                       schema_path: str = "quiz-app/schemas/question_schema.json") -> QuestionLoader:
    """Get global question loader instance."""
    global _question_loader
    
    with _loader_lock:
        if _question_loader is None:
            _question_loader = QuestionLoader(questions_dir, schema_path)
            _question_loader.initialize({})
        return _question_loader