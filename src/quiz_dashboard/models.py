# src/quiz_dashboard/models.py

"""
Database models and schema for Quiz Dashboard application.

This module defines the SQLAlchemy models for questions, users, quiz sessions,
and analytics tracking. Includes comprehensive user performance data and
support for all question types with flexible JSON storage.

Models:
- User: User account and profile information
- Question: Question content with flexible JSON data for different types
- QuizSession: Individual quiz-taking sessions with timing
- QuizAttempt: Individual question attempts with detailed analytics
- UserProgress: Spaced repetition tracking and difficulty adjustment
- QuestionTag: Tagging system for question categorization
"""

import os
import json
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

# Import Framework0 components
from src.core.logger import get_logger

# Initialize module logger
logger = get_logger(__name__)


class QuestionType(Enum):
    """Supported question types in the quiz system."""
    MULTIPLE_CHOICE = "multiple_choice"  # Radio button selection
    TRUE_FALSE = "true_false"  # Boolean validation
    FILL_IN_BLANK = "fill_in_blank"  # Text input with multiple acceptable answers
    REORDER_SEQUENCE = "reorder_sequence"  # Drag-and-drop ordering
    MATCHING_PAIRS = "matching_pairs"  # Left/right pair matching


class DifficultyLevel(Enum):
    """Question difficulty levels for adaptive selection."""
    VERY_EASY = 1
    EASY = 2 
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5


class QuizSessionStatus(Enum):
    """Quiz session status tracking."""
    ACTIVE = "active"  # Currently in progress
    COMPLETED = "completed"  # Finished successfully
    ABANDONED = "abandoned"  # Left incomplete
    PAUSED = "paused"  # Temporarily suspended


@dataclass
class DatabaseConfig:
    """Configuration for database connections and operations."""
    database_path: str = "quiz_dashboard.db"  # SQLite database file path
    connection_timeout: float = 30.0  # Connection timeout in seconds
    enable_foreign_keys: bool = True  # Enable foreign key constraints
    enable_wal_mode: bool = True  # Enable WAL mode for better concurrency
    backup_interval_hours: int = 24  # Automatic backup interval
    max_connections: int = 10  # Maximum concurrent connections
    enable_debugging: bool = False  # Enable SQL query logging


class QuizDatabase:
    """
    Thread-safe SQLite database manager for quiz dashboard.
    
    Provides comprehensive database operations with connection pooling,
    transaction management, and automatic schema creation. Includes
    backup and recovery capabilities.
    """
    
    def __init__(self: 'QuizDatabase', config: DatabaseConfig) -> None:
        # Initialize database manager with configuration settings
        """Initialize database manager with configuration."""
        self.config = config  # Database configuration
        self._connection_lock = threading.Lock()  # Thread safety lock
        self._connections: Dict[int, sqlite3.Connection] = {}  # Connection pool
        self._schema_initialized = False  # Schema creation flag
        
        # Initialize database
        self._initialize_database()
        
        logger.info(f"QuizDatabase initialized: {config.database_path}")
    
    def _initialize_database(self: 'QuizDatabase') -> None:
        # Initialize database with schema and configuration settings
        """Initialize database with schema and configuration."""
        try:
            # Create database directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config.database_path) or ".", exist_ok=True)
            
            # Create initial connection and configure database
            with self._get_connection() as conn:
                # Enable foreign key constraints
                if self.config.enable_foreign_keys:
                    conn.execute("PRAGMA foreign_keys = ON")
                
                # Enable WAL mode for better concurrency
                if self.config.enable_wal_mode:
                    conn.execute("PRAGMA journal_mode = WAL")
                
                # Set other performance optimizations
                conn.execute("PRAGMA synchronous = NORMAL")
                conn.execute("PRAGMA cache_size = 10000")
                conn.execute("PRAGMA temp_store = MEMORY")
                
                # Create schema
                self._create_schema(conn)
                
                conn.commit()
            
            self._schema_initialized = True
            logger.info("Database schema initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _get_connection(self: 'QuizDatabase') -> sqlite3.Connection:
        # Get thread-safe database connection from connection pool
        """Get thread-safe database connection."""
        thread_id = threading.get_ident()
        
        with self._connection_lock:
            if thread_id not in self._connections:
                conn = sqlite3.connect(
                    self.config.database_path,
                    timeout=self.config.connection_timeout,
                    check_same_thread=False
                )
                # Configure connection for optimal performance
                conn.row_factory = sqlite3.Row  # Enable column access by name
                self._connections[thread_id] = conn
            
            return self._connections[thread_id]
    
    def _create_schema(self: 'QuizDatabase', conn: sqlite3.Connection) -> None:
        # Create database schema with all required tables
        """Create database schema with all required tables."""
        
        # Users table - user accounts and profiles
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE,
            password_hash VARCHAR(255),
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP,
            preferences_json TEXT,
            is_active BOOLEAN DEFAULT 1,
            role VARCHAR(20) DEFAULT 'student'
        )""")
        
        # Questions table - question content and metadata
        conn.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_type VARCHAR(20) NOT NULL,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            question_data_json TEXT NOT NULL,
            correct_answer_json TEXT NOT NULL,
            explanation TEXT,
            difficulty_level INTEGER DEFAULT 3,
            estimated_time_seconds INTEGER DEFAULT 60,
            hashtags TEXT,
            latex_content BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )""")
        
        # Quiz sessions table - individual quiz attempts
        conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_uuid VARCHAR(36) UNIQUE NOT NULL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            status VARCHAR(20) DEFAULT 'active',
            total_questions INTEGER DEFAULT 0,
            questions_answered INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            total_time_seconds INTEGER DEFAULT 0,
            session_config_json TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")
        
        # Quiz attempts table - individual question attempts
        conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_answer_json TEXT,
            is_correct BOOLEAN,
            time_taken_seconds REAL,
            difficulty_at_attempt INTEGER,
            confidence_level INTEGER,
            hint_used BOOLEAN DEFAULT 0,
            attempt_number INTEGER DEFAULT 1,
            FOREIGN KEY (session_id) REFERENCES quiz_sessions(id),
            FOREIGN KEY (question_id) REFERENCES questions(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")
        
        # User progress table - spaced repetition and learning analytics
        conn.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            easiness_factor REAL DEFAULT 2.5,
            repetition_count INTEGER DEFAULT 0,
            interval_days INTEGER DEFAULT 1,
            next_review_date DATE,
            last_reviewed_at TIMESTAMP,
            total_attempts INTEGER DEFAULT 0,
            correct_attempts INTEGER DEFAULT 0,
            average_time_seconds REAL DEFAULT 0,
            current_difficulty INTEGER DEFAULT 3,
            mastery_level REAL DEFAULT 0.0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, question_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )""")
        
        # Question tags table - categorization and filtering
        conn.execute("""
        CREATE TABLE IF NOT EXISTS question_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            tag_name VARCHAR(50) NOT NULL,
            tag_value VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions(id),
            UNIQUE(question_id, tag_name)
        )""")
        
        # Performance analytics table - aggregated statistics
        conn.execute("""
        CREATE TABLE IF NOT EXISTS performance_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            analytics_date DATE NOT NULL,
            questions_attempted INTEGER DEFAULT 0,
            questions_correct INTEGER DEFAULT 0,
            average_time_per_question REAL DEFAULT 0,
            difficulty_distribution_json TEXT,
            topic_performance_json TEXT,
            learning_streak_days INTEGER DEFAULT 0,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, analytics_date),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")
        
        # Create indexes for performance optimization
        self._create_indexes(conn)
        
        logger.debug("Database schema created successfully")
    
    def _create_indexes(self: 'QuizDatabase', conn: sqlite3.Connection) -> None:
        # Create database indexes for optimal query performance
        """Create database indexes for optimal query performance."""
        
        indexes = [
            # User-related indexes
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)",
            
            # Question-related indexes
            "CREATE INDEX IF NOT EXISTS idx_questions_type ON questions(question_type)",
            "CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty_level)",
            "CREATE INDEX IF NOT EXISTS idx_questions_active ON questions(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_questions_hashtags ON questions(hashtags)",
            
            # Session-related indexes
            "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON quiz_sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_uuid ON quiz_sessions(session_uuid)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_status ON quiz_sessions(status)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_started ON quiz_sessions(started_at)",
            
            # Attempt-related indexes
            "CREATE INDEX IF NOT EXISTS idx_attempts_session ON quiz_attempts(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_attempts_question ON quiz_attempts(question_id)",
            "CREATE INDEX IF NOT EXISTS idx_attempts_user ON quiz_attempts(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_attempts_attempted ON quiz_attempts(attempted_at)",
            
            # Progress-related indexes
            "CREATE INDEX IF NOT EXISTS idx_progress_user ON user_progress(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_progress_question ON user_progress(question_id)",
            "CREATE INDEX IF NOT EXISTS idx_progress_review_date ON user_progress(next_review_date)",
            "CREATE INDEX IF NOT EXISTS idx_progress_updated ON user_progress(last_updated)",
            
            # Tag-related indexes
            "CREATE INDEX IF NOT EXISTS idx_tags_question ON question_tags(question_id)",
            "CREATE INDEX IF NOT EXISTS idx_tags_name ON question_tags(tag_name)",
            
            # Analytics indexes
            "CREATE INDEX IF NOT EXISTS idx_analytics_user_date ON performance_analytics(user_id, analytics_date)",
        ]
        
        for index_sql in indexes:
            try:
                conn.execute(index_sql)
            except sqlite3.Error as e:
                logger.warning(f"Failed to create index: {e}")
        
        logger.debug("Database indexes created successfully")
    
    def execute_query(self: 'QuizDatabase', query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        # Execute SELECT query and return results with error handling
        """Execute SELECT query and return results."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_update(self: 'QuizDatabase', query: str, params: Tuple = ()) -> int:
        # Execute INSERT/UPDATE/DELETE query and return affected rows count
        """Execute INSERT/UPDATE/DELETE query and return affected rows."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            raise
    
    def close_all_connections(self: 'QuizDatabase') -> None:
        # Close all database connections in the connection pool
        """Close all database connections in the pool."""
        with self._connection_lock:
            for conn in self._connections.values():
                try:
                    conn.close()
                except:
                    pass
            self._connections.clear()
        
        logger.info("All database connections closed")


# Global database instance
_database_instance: Optional[QuizDatabase] = None
_database_lock = threading.Lock()


def get_quiz_database(config: Optional[DatabaseConfig] = None) -> QuizDatabase:
    # Get global quiz database instance using singleton pattern
    """Get global quiz database instance."""
    """Get global quiz database instance."""
    global _database_instance
    
    with _database_lock:
        if _database_instance is None:
            if config is None:
                config = DatabaseConfig()
            _database_instance = QuizDatabase(config)
    
    return _database_instance


def initialize_database(database_path: str = "quiz_dashboard.db") -> QuizDatabase:
    # Initialize quiz database with configuration and return instance
    """Initialize quiz database with default configuration."""
    """Initialize quiz database with custom path."""
    config = DatabaseConfig(database_path=database_path)
    return get_quiz_database(config)