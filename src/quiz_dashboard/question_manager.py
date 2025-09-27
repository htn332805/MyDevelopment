# src/quiz_dashboard/question_manager.py

"""
Question management system with JSON schema validation.

This module handles creation, validation, storage, and retrieval of quiz questions
across all supported types. Includes comprehensive JSON schema validation,
question format standardization, and flexible content management.

Features:
- JSON schema validation for all question types
- Question import/export with validation
- LaTeX content detection and processing
- Hashtag management and search
- Question difficulty assessment
- Content sanitization and security
"""

import os
import json
import re
import hashlib
import uuid
import threading
from typing import Dict, Any, List, Optional, Union, Tuple, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
import jsonschema
from jsonschema import validate, ValidationError

# Import Framework0 components
from src.core.logger import get_logger
from .models import QuizDatabase, get_quiz_database, QuestionType, DifficultyLevel

# Initialize module logger
logger = get_logger(__name__)


@dataclass
class QuestionValidationResult:
    """Result of question validation process."""
    is_valid: bool  # Whether question passes all validation
    errors: List[str] = field(default_factory=list)  # Validation error messages
    warnings: List[str] = field(default_factory=list)  # Non-critical warnings
    suggestions: List[str] = field(default_factory=list)  # Improvement suggestions
    estimated_difficulty: Optional[int] = None  # Auto-estimated difficulty
    detected_topics: List[str] = field(default_factory=list)  # Auto-detected topics
    latex_content: bool = False  # Whether LaTeX content detected


class QuestionSchemaValidator:
    """
    JSON schema validator for quiz questions.
    
    Provides comprehensive validation for all question types with detailed
    error reporting and content analysis capabilities.
    """
    
    def __init__(self) -> None:
        # Initialize schema validator with question type schemas
        """Initialize schema validator with question type schemas."""
        self.schemas = self._load_question_schemas()  # Question type schemas
        self.latex_pattern = re.compile(r'\$.*?\$|\\\(.*?\\\)|\\\[.*?\\\]|\\begin\{.*?\}.*?\\end\{.*?\}', re.DOTALL)
        
        logger.debug("QuestionSchemaValidator initialized")
    
    def _load_question_schemas(self) -> Dict[str, Dict[str, Any]]:
        # Load JSON schemas for all question types
        """Load JSON schemas for all question types."""
        
        # Base question schema - common fields for all types
        base_schema = {
            "type": "object",
            "required": ["id", "type", "title", "content"],
            "properties": {
                "id": {"type": "string", "minLength": 1},
                "type": {"type": "string", "enum": [t.value for t in QuestionType]},
                "title": {"type": "string", "minLength": 1, "maxLength": 200},
                "content": {"type": "string", "minLength": 1},
                "explanation": {"type": "string"},
                "difficulty": {"type": "integer", "minimum": 1, "maximum": 5},
                "estimated_time": {"type": "integer", "minimum": 5, "maximum": 3600},
                "hashtags": {"type": "array", "items": {"type": "string"}},
                "metadata": {"type": "object"}
            }
        }
        
        # Multiple choice question schema
        multiple_choice_schema = {
            **base_schema,
            "required": base_schema["required"] + ["options", "correct_answer"],
            "properties": {
                **base_schema["properties"],
                "options": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 8,
                    "items": {
                        "type": "object",
                        "required": ["id", "text"],
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string", "minLength": 1},
                            "explanation": {"type": "string"}
                        }
                    }
                },
                "correct_answer": {"type": "string"},
                "allow_multiple": {"type": "boolean", "default": False},
                "shuffle_options": {"type": "boolean", "default": True}
            }
        }
        
        # True/False question schema
        true_false_schema = {
            **base_schema,
            "required": base_schema["required"] + ["correct_answer"],
            "properties": {
                **base_schema["properties"],
                "correct_answer": {"type": "boolean"},
                "true_explanation": {"type": "string"},
                "false_explanation": {"type": "string"}
            }
        }
        
        # Fill-in-the-blank question schema
        fill_in_blank_schema = {
            **base_schema,
            "required": base_schema["required"] + ["acceptable_answers"],
            "properties": {
                **base_schema["properties"],
                "acceptable_answers": {
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string", "minLength": 1}
                },
                "case_sensitive": {"type": "boolean", "default": False},
                "partial_credit": {"type": "boolean", "default": False},
                "blank_placeholder": {"type": "string", "default": "_____"}
            }
        }
        
        # Reorder/Sequence question schema
        reorder_schema = {
            **base_schema,
            "required": base_schema["required"] + ["items", "correct_order"],
            "properties": {
                **base_schema["properties"],
                "items": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 10,
                    "items": {
                        "type": "object",
                        "required": ["id", "text"],
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string", "minLength": 1},
                            "description": {"type": "string"}
                        }
                    }
                },
                "correct_order": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "partial_credit": {"type": "boolean", "default": True}
            }
        }
        
        # Matching pairs question schema
        matching_schema = {
            **base_schema,
            "required": base_schema["required"] + ["left_items", "right_items", "correct_matches"],
            "properties": {
                **base_schema["properties"],
                "left_items": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 8,
                    "items": {
                        "type": "object",
                        "required": ["id", "text"],
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string", "minLength": 1}
                        }
                    }
                },
                "right_items": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 8,
                    "items": {
                        "type": "object",
                        "required": ["id", "text"],
                        "properties": {
                            "id": {"type": "string"},
                            "text": {"type": "string", "minLength": 1}
                        }
                    }
                },
                "correct_matches": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["left_id", "right_id"],
                        "properties": {
                            "left_id": {"type": "string"},
                            "right_id": {"type": "string"}
                        }
                    }
                },
                "allow_multiple_matches": {"type": "boolean", "default": False}
            }
        }
        
        return {
            QuestionType.MULTIPLE_CHOICE.value: multiple_choice_schema,
            QuestionType.TRUE_FALSE.value: true_false_schema,
            QuestionType.FILL_IN_BLANK.value: fill_in_blank_schema,
            QuestionType.REORDER_SEQUENCE.value: reorder_schema,
            QuestionType.MATCHING_PAIRS.value: matching_schema
        }
    
    def validate_question(self, question_data: Dict[str, Any]) -> QuestionValidationResult:
        # Validate question data against appropriate schema
        """Validate question data against appropriate schema."""
        result = QuestionValidationResult(is_valid=False)
        
        try:
            # Check if question type is specified and supported
            question_type = question_data.get("type")
            if not question_type:
                result.errors.append("Question type is required")
                return result
            
            if question_type not in self.schemas:
                result.errors.append(f"Unsupported question type: {question_type}")
                return result
            
            # Validate against question type schema
            schema = self.schemas[question_type]
            validate(instance=question_data, schema=schema)
            
            # Additional validation checks
            self._validate_content_quality(question_data, result)
            self._detect_latex_content(question_data, result)
            self._estimate_difficulty(question_data, result)
            self._detect_topics(question_data, result)
            
            # Check for common issues
            self._check_common_issues(question_data, result)
            
            result.is_valid = len(result.errors) == 0
            
            if result.is_valid:
                logger.debug(f"Question validation successful: {question_data.get('title', 'Untitled')}")
            else:
                logger.warning(f"Question validation failed: {result.errors}")
            
        except ValidationError as e:
            result.errors.append(f"Schema validation error: {e.message}")
            logger.error(f"JSON schema validation failed: {e}")
        except Exception as e:
            result.errors.append(f"Validation error: {str(e)}")
            logger.error(f"Question validation error: {e}")
        
        return result
    
    def _validate_content_quality(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Validate content quality and completeness
        """Validate content quality and completeness."""
        
        # Check title length and quality
        title = question_data.get("title", "")
        if len(title) < 5:
            result.warnings.append("Title is very short, consider making it more descriptive")
        elif len(title) > 150:
            result.warnings.append("Title is quite long, consider shortening for clarity")
        
        # Check content length
        content = question_data.get("content", "")
        if len(content) < 10:
            result.warnings.append("Question content is very short")
        elif len(content) > 2000:
            result.warnings.append("Question content is quite long, consider breaking into parts")
        
        # Check for explanation
        if not question_data.get("explanation"):
            result.suggestions.append("Consider adding an explanation to help students learn")
        
        # Type-specific content validation
        question_type = question_data.get("type")
        
        if question_type == QuestionType.MULTIPLE_CHOICE.value:
            self._validate_multiple_choice_quality(question_data, result)
        elif question_type == QuestionType.FILL_IN_BLANK.value:
            self._validate_fill_in_blank_quality(question_data, result)
        elif question_type == QuestionType.REORDER_SEQUENCE.value:
            self._validate_reorder_quality(question_data, result)
        elif question_type == QuestionType.MATCHING_PAIRS.value:
            self._validate_matching_quality(question_data, result)
    
    def _validate_multiple_choice_quality(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Validate multiple choice question quality
        """Validate multiple choice question quality."""
        options = question_data.get("options", [])
        correct_answer = question_data.get("correct_answer")
        
        # Check option count
        if len(options) < 3:
            result.warnings.append("Consider having at least 3 options for multiple choice")
        elif len(options) > 6:
            result.warnings.append("Too many options may confuse students")
        
        # Check option length consistency
        option_lengths = [len(opt.get("text", "")) for opt in options]
        if max(option_lengths) - min(option_lengths) > 100:
            result.warnings.append("Option lengths vary significantly, try to balance them")
        
        # Check if correct answer exists in options
        option_ids = {opt.get("id") for opt in options}
        if correct_answer not in option_ids:
            result.errors.append("Correct answer ID does not match any option ID")
    
    def _validate_fill_in_blank_quality(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Validate fill-in-blank question quality
        """Validate fill-in-blank question quality."""
        acceptable_answers = question_data.get("acceptable_answers", [])
        
        if len(acceptable_answers) < 1:
            result.errors.append("At least one acceptable answer is required")
        
        # Check for variety in acceptable answers
        if len(set(answer.lower() for answer in acceptable_answers)) < len(acceptable_answers):
            result.warnings.append("Some acceptable answers are duplicates (case-insensitive)")
    
    def _validate_reorder_quality(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Validate reorder/sequence question quality
        """Validate reorder/sequence question quality."""
        items = question_data.get("items", [])
        correct_order = question_data.get("correct_order", [])
        
        # Check item count
        if len(items) < 3:
            result.warnings.append("Consider having at least 3 items for reordering")
        elif len(items) > 8:
            result.warnings.append("Too many items may be overwhelming for students")
        
        # Validate correct order matches items
        item_ids = {item.get("id") for item in items}
        order_ids = set(correct_order)
        
        if item_ids != order_ids:
            result.errors.append("Correct order IDs do not match item IDs")
    
    def _validate_matching_quality(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Validate matching pairs question quality
        """Validate matching pairs question quality."""
        left_items = question_data.get("left_items", [])
        right_items = question_data.get("right_items", [])
        correct_matches = question_data.get("correct_matches", [])
        
        # Check balance between left and right items
        if abs(len(left_items) - len(right_items)) > 2:
            result.warnings.append("Left and right items should be roughly balanced")
        
        # Validate matches reference existing items
        left_ids = {item.get("id") for item in left_items}
        right_ids = {item.get("id") for item in right_items}
        
        for match in correct_matches:
            left_id = match.get("left_id")
            right_id = match.get("right_id")
            
            if left_id not in left_ids:
                result.errors.append(f"Match references non-existent left item: {left_id}")
            if right_id not in right_ids:
                result.errors.append(f"Match references non-existent right item: {right_id}")
    
    def _detect_latex_content(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Detect LaTeX mathematical content in question
        """Detect LaTeX mathematical content in question."""
        
        # Check all text fields for LaTeX patterns
        text_fields = []
        
        # Add basic fields
        text_fields.extend([
            question_data.get("title", ""),
            question_data.get("content", ""),
            question_data.get("explanation", "")
        ])
        
        # Add type-specific fields
        question_type = question_data.get("type")
        
        if question_type == QuestionType.MULTIPLE_CHOICE.value:
            for option in question_data.get("options", []):
                text_fields.append(option.get("text", ""))
                text_fields.append(option.get("explanation", ""))
        
        # Check for LaTeX patterns
        has_latex = any(self.latex_pattern.search(text) for text in text_fields if text)
        result.latex_content = has_latex
        
        if has_latex:
            result.suggestions.append("LaTeX content detected - ensure MathJax is enabled")
    
    def _estimate_difficulty(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Estimate question difficulty based on content analysis
        """Estimate question difficulty based on content analysis."""
        
        difficulty_score = 3  # Default medium difficulty
        
        # Analyze content complexity
        content = question_data.get("content", "")
        
        # Length-based factors
        if len(content) > 500:
            difficulty_score += 1
        elif len(content) < 100:
            difficulty_score -= 1
        
        # LaTeX content increases difficulty
        if result.latex_content:
            difficulty_score += 1
        
        # Question type complexity
        question_type = question_data.get("type")
        type_complexity = {
            QuestionType.TRUE_FALSE.value: -1,
            QuestionType.MULTIPLE_CHOICE.value: 0,
            QuestionType.FILL_IN_BLANK.value: 1,
            QuestionType.MATCHING_PAIRS.value: 1,
            QuestionType.REORDER_SEQUENCE.value: 2
        }
        
        difficulty_score += type_complexity.get(question_type, 0)
        
        # Clamp to valid range
        result.estimated_difficulty = max(1, min(5, difficulty_score))
    
    def _detect_topics(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Detect topics/subjects from question content
        """Detect topics/subjects from question content."""
        
        # Common academic topics/keywords
        topic_keywords = {
            "mathematics": ["math", "equation", "formula", "calculate", "solve", "algebra", "geometry", "trigonometry"],
            "science": ["experiment", "hypothesis", "theory", "observation", "analysis", "research"],
            "physics": ["force", "energy", "motion", "velocity", "acceleration", "mass", "gravity"],
            "chemistry": ["molecule", "atom", "reaction", "compound", "element", "solution"],
            "biology": ["cell", "organism", "evolution", "genetics", "ecosystem", "species"],
            "history": ["century", "ancient", "medieval", "war", "civilization", "empire", "revolution"],
            "literature": ["author", "novel", "poem", "character", "plot", "theme", "metaphor"],
            "geography": ["continent", "country", "climate", "population", "capital", "region"]
        }
        
        # Combine all text content
        all_text = " ".join([
            question_data.get("title", ""),
            question_data.get("content", ""),
            question_data.get("explanation", "")
        ]).lower()
        
        # Check for topic keywords
        detected_topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                detected_topics.append(topic)
        
        result.detected_topics = detected_topics
    
    def _check_common_issues(self, question_data: Dict[str, Any], result: QuestionValidationResult) -> None:
        # Check for common question authoring issues
        """Check for common question authoring issues."""
        
        title = question_data.get("title", "").lower()
        content = question_data.get("content", "").lower()
        
        # Check for unclear language
        unclear_words = ["maybe", "possibly", "might", "could be", "probably"]
        if any(word in content for word in unclear_words):
            result.warnings.append("Question contains potentially unclear language")
        
        # Check for absolute statements that may be problematic
        absolute_words = ["always", "never", "all", "none", "every", "completely"]
        if any(word in content for word in absolute_words):
            result.suggestions.append("Be careful with absolute statements - consider exceptions")
        
        # Check question format
        if not content.strip().endswith("?") and question_data.get("type") != QuestionType.FILL_IN_BLANK.value:
            result.suggestions.append("Consider ending questions with a question mark")


class QuestionManager:
    """
    Comprehensive question management system.
    
    Handles question CRUD operations, validation, import/export,
    and search functionality with database integration.
    """
    
    def __init__(self: 'QuestionManager', database: Optional[QuizDatabase] = None) -> None:
        # Initialize question manager with database connection
        """Initialize question manager with database connection."""
        self.database = database or get_quiz_database()  # Database connection
        self.validator = QuestionSchemaValidator()  # Schema validator
        
        logger.info("QuestionManager initialized")
    
    def create_question(self, question_data: Dict[str, Any], created_by: Optional[int] = None) -> Optional[int]:
        # Create new question with validation
        """Create new question with validation."""
        
        try:
            # Validate question data
            validation_result = self.validator.validate_question(question_data)
            
            if not validation_result.is_valid:
                logger.error(f"Question validation failed: {validation_result.errors}")
                return None
            
            # Extract and prepare data for database
            question_id = str(uuid.uuid4())
            question_type = question_data["type"]
            title = question_data["title"]
            content = question_data["content"]
            
            # Prepare question data JSON (remove base fields)
            question_data_json = {k: v for k, v in question_data.items() 
                                if k not in ["id", "type", "title", "content", "explanation"]}
            
            # Prepare correct answer JSON
            correct_answer_json = self._extract_correct_answer(question_data)
            
            # Database insertion
            query = """
                INSERT INTO questions (
                    question_type, title, content, question_data_json, 
                    correct_answer_json, explanation, difficulty_level,
                    estimated_time_seconds, hashtags, latex_content, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                question_type,
                title,
                content,
                json.dumps(question_data_json),
                json.dumps(correct_answer_json),
                question_data.get("explanation"),
                validation_result.estimated_difficulty or question_data.get("difficulty", 3),
                question_data.get("estimated_time", 60),
                json.dumps(question_data.get("hashtags", [])),
                validation_result.latex_content,
                created_by
            )
            
            affected_rows = self.database.execute_update(query, params)
            
            if affected_rows > 0:
                # Get the inserted question ID
                result = self.database.execute_query("SELECT last_insert_rowid()")
                db_question_id = result[0][0]
                
                # Add tags if any
                self._add_question_tags(db_question_id, question_data.get("hashtags", []))
                
                logger.info(f"Question created successfully: {title} (ID: {db_question_id})")
                return db_question_id
            else:
                logger.error("Failed to insert question into database")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create question: {e}")
            return None
    
    def _extract_correct_answer(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        # Extract correct answer data based on question type
        """Extract correct answer data based on question type."""
        
        question_type = question_data["type"]
        
        if question_type == QuestionType.MULTIPLE_CHOICE.value:
            return {"correct_answer": question_data["correct_answer"]}
        elif question_type == QuestionType.TRUE_FALSE.value:
            return {"correct_answer": question_data["correct_answer"]}
        elif question_type == QuestionType.FILL_IN_BLANK.value:
            return {
                "acceptable_answers": question_data["acceptable_answers"],
                "case_sensitive": question_data.get("case_sensitive", False)
            }
        elif question_type == QuestionType.REORDER_SEQUENCE.value:
            return {"correct_order": question_data["correct_order"]}
        elif question_type == QuestionType.MATCHING_PAIRS.value:
            return {"correct_matches": question_data["correct_matches"]}
        
        return {}
    
    def _add_question_tags(self, question_id: int, hashtags: List[str]) -> None:
        # Add hashtags as question tags
        """Add hashtags as question tags."""
        
        for tag in hashtags:
            try:
                query = "INSERT OR IGNORE INTO question_tags (question_id, tag_name) VALUES (?, ?)"
                self.database.execute_update(query, (question_id, tag))
            except Exception as e:
                logger.warning(f"Failed to add tag '{tag}': {e}")
    
    def get_question(self, question_id: int) -> Optional[Dict[str, Any]]:
        # Retrieve question by ID
        """Retrieve question by ID."""
        
        try:
            query = """
                SELECT id, question_type, title, content, question_data_json,
                       correct_answer_json, explanation, difficulty_level,
                       estimated_time_seconds, hashtags, latex_content,
                       created_at, updated_at, is_active
                FROM questions
                WHERE id = ? AND is_active = 1
            """
            
            results = self.database.execute_query(query, (question_id,))
            
            if not results:
                return None
            
            row = results[0]
            
            # Build complete question data
            question_data = {
                "id": str(row["id"]),
                "type": row["question_type"],
                "title": row["title"],
                "content": row["content"],
                "explanation": row["explanation"],
                "difficulty": row["difficulty_level"],
                "estimated_time": row["estimated_time_seconds"],
                "hashtags": json.loads(row["hashtags"]) if row["hashtags"] else [],
                "latex_content": bool(row["latex_content"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            
            # Add question-specific data
            question_specific_data = json.loads(row["question_data_json"])
            question_data.update(question_specific_data)
            
            return question_data
            
        except Exception as e:
            logger.error(f"Failed to retrieve question {question_id}: {e}")
            return None
    
    def search_questions(self, 
                        question_type: Optional[str] = None,
    """Execute search_questions operation."""
                        hashtags: Optional[List[str]] = None,
                        difficulty_range: Optional[Tuple[int, int]] = None,
                        search_text: Optional[str] = None,
                        limit: int = 50) -> List[Dict[str, Any]]:
        # Execute search_questions operation
        # search_questions operation implementation
        """Search questions with filters."""
        
        try:
            # Build query with filters
            conditions = ["is_active = 1"]
            params = []
            
            if question_type:
                conditions.append("question_type = ?")
                params.append(question_type)
            
            if hashtags:
                hashtag_conditions = []
                for tag in hashtags:
                    hashtag_conditions.append("hashtags LIKE ?")
                    params.append(f"%\"{tag}\"%")
                conditions.append(f"({' OR '.join(hashtag_conditions)})")
            
            if difficulty_range:
                conditions.append("difficulty_level BETWEEN ? AND ?")
                params.extend(difficulty_range)
            
            if search_text:
                conditions.append("(title LIKE ? OR content LIKE ?)")
                search_param = f"%{search_text}%"
                params.extend([search_param, search_param])
            
            query = f"""
                SELECT id, question_type, title, content, explanation, 
                       difficulty_level, hashtags, latex_content
                FROM questions
                WHERE {' AND '.join(conditions)}
                ORDER BY created_at DESC
                LIMIT ?
            """
            params.append(limit)
            
            results = self.database.execute_query(query, tuple(params))
            
            questions = []
            for row in results:
                question = {
                    "id": row["id"],
                    "type": row["question_type"],
                    "title": row["title"],
                    "content": row["content"][:200] + "..." if len(row["content"]) > 200 else row["content"],
                    "explanation": row["explanation"],
                    "difficulty": row["difficulty_level"],
                    "hashtags": json.loads(row["hashtags"]) if row["hashtags"] else [],
                    "latex_content": bool(row["latex_content"])
                }
                questions.append(question)
            
            logger.debug(f"Found {len(questions)} questions matching search criteria")
            return questions
            
        except Exception as e:
            logger.error(f"Question search failed: {e}")
            return []
    
    def import_questions(self, questions_file: str) -> Dict[str, Any]:
        # Import questions from JSON file with validation
        """Import questions from JSON file with validation."""
        
        result = {
            "total": 0,
            "imported": 0,
            "errors": [],
            "warnings": []
        }
        
        try:
            with open(questions_file, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
            
            if not isinstance(questions_data, list):
                questions_data = [questions_data]
            
            result["total"] = len(questions_data)
            
            for i, question_data in enumerate(questions_data):
                try:
                    question_id = self.create_question(question_data)
                    if question_id:
                        result["imported"] += 1
                    else:
                        result["errors"].append(f"Question {i+1}: Failed to create question")
                        
                except Exception as e:
                    result["errors"].append(f"Question {i+1}: {str(e)}")
            
            logger.info(f"Question import completed: {result['imported']}/{result['total']} successful")
            
        except Exception as e:
            result["errors"].append(f"Failed to read questions file: {str(e)}")
            logger.error(f"Question import failed: {e}")
        
        return result


# Global question manager instance
_question_manager: Optional[QuestionManager] = None
_manager_lock = threading.Lock()


def get_question_manager(database: Optional[QuizDatabase] = None) -> QuestionManager:
        # Get global question manager instance
    """Get global question manager instance."""
    global _question_manager
    
    with _manager_lock:
        if _question_manager is None:
            _question_manager = QuestionManager(database)
    
    return _question_manager