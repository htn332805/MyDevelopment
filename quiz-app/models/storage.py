# quiz-app/models/storage.py

"""
Database storage and ORM models for the quiz application.

This module provides comprehensive database operations including:
- SQLite database schema creation and management
- User management with authentication support
- Question metadata caching for performance
- Attempt tracking with detailed analytics
- Spaced repetition algorithm implementation
- Performance metrics and statistics

Integrates with Framework0's storage system for consistency.
"""

import sqlite3
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
import threading

# Import Framework0 components for consistency
from src.core.logger import get_logger
from src.core.interfaces import ComponentLifecycle, Configurable
from src.core.decorators_v2 import monitor_resources, debug_trace

# Initialize logger with debug support
logger = get_logger(__name__, debug=True)


@dataclass
class QuestionStats:
    """Question performance statistics for spaced repetition."""
    question_id: str  # Unique question identifier
    total_seen: int = 0  # Total times question was shown
    total_correct: int = 0  # Total correct answers
    last_seen: Optional[datetime] = None  # Last time question was shown
    last_correct: Optional[datetime] = None  # Last time answered correctly
    weight: float = 1.0  # Dynamic priority weight for selection
    ease_factor: float = 2.5  # SM-2 algorithm ease factor
    interval: int = 1  # Days until next review
    streak: int = 0  # Current consecutive correct answers


@dataclass
class UserAttempt:
    """Individual user attempt record."""
    attempt_id: str  # Unique attempt identifier
    user_id: int  # User who made the attempt
    question_id: str  # Question that was attempted
    timestamp: datetime  # When attempt was made
    correct: bool  # Whether answer was correct
    response: str  # User's raw response
    latency: float  # Time taken in seconds
    hint_used: bool = False  # Whether hint was viewed
    streak: int = 0  # Streak after this attempt
    ease_factor: float = 2.5  # SM-2 ease factor snapshot
    interval: int = 1  # Suggested next interval


class QuizDatabase(ComponentLifecycle, Configurable):
    """
    Main database interface for quiz application.
    
    Provides thread-safe access to SQLite database with automatic
    connection management, schema creation, and query optimization.
    """
    
    def __init__(self, db_path: str = "quiz-app/data/db/quiz.sqlite"):
        """Initialize database connection and schema."""
        super().__init__()
        self.db_path = Path(db_path)  # Database file path
        self.db_lock = threading.Lock()  # Thread safety lock
        self._connection_cache = {}  # Thread-local connections
        
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Initialize database schema and connections."""
        logger.info(f"Initializing quiz database at {self.db_path}")
        
        # Create database directory if needed
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database schema
        self._create_schema()
        
        logger.info("Quiz database initialized successfully")
        
    def _do_cleanup(self) -> None:
        """Clean up database connections and resources."""
        logger.info("Cleaning up quiz database connections")
        
        # Close all cached connections
        for conn in self._connection_cache.values():
            if conn:
                conn.close()
        self._connection_cache.clear()
        
        logger.info("Quiz database cleanup completed")
    
    def get_connection(self) -> sqlite3.Connection:
        """Get thread-safe database connection."""
        thread_id = threading.get_ident()  # Get current thread ID
        
        # Return cached connection for this thread
        if thread_id in self._connection_cache:
            return self._connection_cache[thread_id]
        
        # Create new connection for this thread
        with self.db_lock:
            conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            conn.row_factory = sqlite3.Row  # Enable dict-like row access
            self._connection_cache[thread_id] = conn
            return conn
    
    @monitor_resources
    def _create_schema(self) -> None:
        """Create database schema if it doesn't exist."""
        conn = self.get_connection()  # Get database connection
        
        try:
            # Create questions metadata table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    question_id TEXT PRIMARY KEY,
                    qtype TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    categories TEXT,  -- JSON array as TEXT
                    hashtags TEXT,    -- JSON array as TEXT
                    difficulty TEXT DEFAULT 'medium',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create users table with authentication
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_login DATETIME,
                    preferences TEXT  -- JSON configuration
                )
            """)
            
            # Create attempts table for detailed tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS attempts (
                    attempt_id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    question_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    correct INTEGER NOT NULL,  -- 1 or 0
                    response TEXT NOT NULL,     -- User's raw response
                    latency REAL NOT NULL,      -- Seconds spent
                    hint_used INTEGER DEFAULT 0, -- Whether hint was used
                    streak INTEGER DEFAULT 0,   -- Consecutive correct after this
                    ease_factor REAL DEFAULT 2.5, -- SM-2 snapshot
                    interval INTEGER DEFAULT 1,   -- Days until next review
                    FOREIGN KEY(question_id) REFERENCES questions(question_id),
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            
            # Create question statistics for performance tracking
            conn.execute("""
                CREATE TABLE IF NOT EXISTS question_stats (
                    question_id TEXT PRIMARY KEY,
                    total_seen INTEGER DEFAULT 0,
                    total_correct INTEGER DEFAULT 0,
                    last_seen DATETIME,
                    last_correct DATETIME,
                    weight REAL DEFAULT 1.0,    -- Dynamic priority weight
                    ease_factor REAL DEFAULT 2.5, -- SM-2 ease factor
                    interval INTEGER DEFAULT 1,   -- Days until next review
                    FOREIGN KEY(question_id) REFERENCES questions(question_id)
                )
            """)
            
            # Create indexes for query performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_attempts_user ON attempts(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_attempts_question ON attempts(question_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_attempts_timestamp ON attempts(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(categories)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty)")
            
            # Create default user if none exists
            self._create_default_user(conn)
            
            conn.commit()  # Commit schema changes
            logger.debug("Database schema created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create database schema: {e}")
            conn.rollback()  # Rollback on error
            raise
    
    def _create_default_user(self, conn: sqlite3.Connection) -> None:
        """Create default user account if none exists."""
        try:
            # Check if any users exist
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            
            # Create default user if none exist
            if user_count == 0:
                conn.execute("""
                    INSERT INTO users (username, email, preferences)
                    VALUES (?, ?, ?)
                """, ('default', 'default@quiz.local', '{}'))
                
                logger.info("Created default user account")
                
        except Exception as e:
            logger.error(f"Failed to create default user: {e}")
    
    @monitor_resources
    @debug_trace
    def store_question_metadata(self, question_data: Dict[str, Any]) -> bool:
        """Store question metadata for quick access."""
        conn = self.get_connection()  # Get database connection
        
        try:
            # Extract question metadata
            question_id = str(question_data['question_id'])
            qtype = question_data['type']
            prompt = question_data['prompt']
            categories = json.dumps(question_data.get('categories', []))
            hashtags = json.dumps(question_data.get('hashtags', []))
            difficulty = question_data.get('difficulty', 'medium')
            
            # Insert or replace question metadata
            conn.execute("""
                INSERT OR REPLACE INTO questions 
                (question_id, qtype, prompt, categories, hashtags, difficulty, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (question_id, qtype, prompt, categories, hashtags, difficulty))
            
            # Initialize question statistics if not exists
            conn.execute("""
                INSERT OR IGNORE INTO question_stats (question_id)
                VALUES (?)
            """, (question_id,))
            
            conn.commit()  # Commit changes
            logger.debug(f"Stored metadata for question {question_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store question metadata: {e}")
            conn.rollback()  # Rollback on error
            return False
    
    @monitor_resources
    def record_attempt(self, user_id: int, question_id: str, correct: bool, 
                      response: str, latency: float, hint_used: bool = False) -> str:
        """Record a user attempt and update statistics."""
        conn = self.get_connection()  # Get database connection
        attempt_id = str(uuid.uuid4())  # Generate unique attempt ID
        
        try:
            # Get current question stats for SM-2 calculation
            stats = self.get_question_stats(question_id)
            
            # Update streak and SM-2 algorithm parameters
            new_streak = stats.streak + 1 if correct else 0
            new_ease_factor = self._calculate_ease_factor(stats.ease_factor, correct)
            new_interval = self._calculate_interval(stats.interval, new_ease_factor, correct)
            
            # Record the attempt
            conn.execute("""
                INSERT INTO attempts 
                (attempt_id, user_id, question_id, correct, response, latency, 
                 hint_used, streak, ease_factor, interval)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (attempt_id, user_id, question_id, int(correct), response, 
                  latency, int(hint_used), new_streak, new_ease_factor, new_interval))
            
            # Update question statistics
            self._update_question_stats(conn, question_id, correct, new_streak, 
                                      new_ease_factor, new_interval)
            
            conn.commit()  # Commit all changes
            logger.debug(f"Recorded attempt {attempt_id} for question {question_id}")
            return attempt_id
            
        except Exception as e:
            logger.error(f"Failed to record attempt: {e}")
            conn.rollback()  # Rollback on error
            raise
    
    def _update_question_stats(self, conn: sqlite3.Connection, question_id: str, 
                             correct: bool, streak: int, ease_factor: float, 
                             interval: int) -> None:
        """Update question statistics after an attempt."""
        try:
            # Calculate new weight based on performance
            weight = self._calculate_weight(question_id, correct)
            
            # Update question statistics
            conn.execute("""
                UPDATE question_stats SET
                    total_seen = total_seen + 1,
                    total_correct = total_correct + ?,
                    last_seen = CURRENT_TIMESTAMP,
                    last_correct = CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE last_correct END,
                    weight = ?,
                    ease_factor = ?,
                    interval = ?
                WHERE question_id = ?
            """, (int(correct), int(correct), weight, ease_factor, interval, question_id))
            
            logger.debug(f"Updated stats for question {question_id}")
            
        except Exception as e:
            logger.error(f"Failed to update question stats: {e}")
            raise
    
    def _calculate_ease_factor(self, current_ease: float, correct: bool) -> float:
        """Calculate SM-2 ease factor based on performance."""
        if correct:
            # Increase ease factor for correct answers (max 3.0)
            return min(3.0, current_ease + 0.1)
        else:
            # Decrease ease factor for incorrect answers (min 1.3)
            return max(1.3, current_ease - 0.2)
    
    def _calculate_interval(self, current_interval: int, ease_factor: float, 
                          correct: bool) -> int:
        """Calculate next review interval using SM-2 algorithm."""
        if not correct:
            return 1  # Reset to 1 day for incorrect answers
        
        if current_interval == 1:
            return 6  # Second review after 6 days
        else:
            # Subsequent intervals based on ease factor
            return max(1, int(current_interval * ease_factor))
    
    def _calculate_weight(self, question_id: str, correct: bool) -> float:
        """Calculate dynamic weight for question selection."""
        stats = self.get_question_stats(question_id)  # Get current statistics
        
        # Base weight from difficulty
        difficulty_weights = {'easy': 1.0, 'medium': 2.0, 'hard': 3.0}
        base_weight = difficulty_weights.get(self._get_question_difficulty(question_id), 2.0)
        
        # Error factor - increase weight for questions often answered incorrectly
        if stats.total_seen > 0:
            error_rate = (stats.total_seen - stats.total_correct) / stats.total_seen
            error_factor = 1.0 + error_rate * 2.0  # Up to 3x weight for 100% error rate
        else:
            error_factor = 1.0
        
        # Recency factor - boost recently missed questions
        recency_factor = 1.0
        if stats.last_seen and not correct:
            days_since = (datetime.now() - stats.last_seen).days
            if days_since <= 7:  # Boost recently missed questions
                recency_factor = 2.0
        
        return base_weight * error_factor * recency_factor
    
    def _get_question_difficulty(self, question_id: str) -> str:
        """Get question difficulty from metadata."""
        conn = self.get_connection()  # Get database connection
        try:
            cursor = conn.execute(
                "SELECT difficulty FROM questions WHERE question_id = ?", 
                (question_id,)
            )
            row = cursor.fetchone()
            return row['difficulty'] if row else 'medium'
        except Exception:
            return 'medium'  # Default difficulty
    
    @monitor_resources
    def get_question_stats(self, question_id: str) -> QuestionStats:
        """Retrieve question statistics."""
        conn = self.get_connection()  # Get database connection
        
        try:
            cursor = conn.execute("""
                SELECT * FROM question_stats WHERE question_id = ?
            """, (question_id,))
            row = cursor.fetchone()
            
            if row:
                return QuestionStats(
                    question_id=row['question_id'],
                    total_seen=row['total_seen'],
                    total_correct=row['total_correct'],
                    last_seen=datetime.fromisoformat(row['last_seen']) if row['last_seen'] else None,
                    last_correct=datetime.fromisoformat(row['last_correct']) if row['last_correct'] else None,
                    weight=row['weight'],
                    ease_factor=row['ease_factor'],
                    interval=row['interval'],
                    streak=0  # Calculate from recent attempts
                )
            else:
                # Return default stats for new questions
                return QuestionStats(question_id=question_id)
                
        except Exception as e:
            logger.error(f"Failed to get question stats: {e}")
            return QuestionStats(question_id=question_id)  # Return default
    
    @monitor_resources
    def get_weighted_question_candidates(self, user_id: int, categories: Optional[List[str]] = None,
                                       hashtags: Optional[List[str]] = None,
                                       limit: int = 50) -> List[Tuple[str, float]]:
        """Get weighted question candidates for quiz selection."""
        conn = self.get_connection()  # Get database connection
        
        try:
            # Build query with filters
            query = """
                SELECT q.question_id, qs.weight, q.categories, q.hashtags
                FROM questions q
                JOIN question_stats qs ON q.question_id = qs.question_id
                WHERE 1=1
            """
            params = []
            
            # Add category filter
            if categories:
                category_conditions = []
                for category in categories:
                    category_conditions.append("q.categories LIKE ?")
                    params.append(f'%"{category}"%')
                query += f" AND ({' OR '.join(category_conditions)})"
            
            # Add hashtag filter
            if hashtags:
                hashtag_conditions = []
                for hashtag in hashtags:
                    hashtag_conditions.append("q.hashtags LIKE ?")
                    params.append(f'%"{hashtag}"%')
                query += f" AND ({' OR '.join(hashtag_conditions)})"
            
            # Order by weight descending
            query += " ORDER BY qs.weight DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            
            # Return list of (question_id, weight) tuples
            candidates = []
            for row in rows:
                question_id = row['question_id']
                weight = row['weight']
                
                # Apply hashtag multiplier if requested
                if hashtags:
                    question_hashtags = json.loads(row['hashtags'] or '[]')
                    if any(tag in question_hashtags for tag in hashtags):
                        weight *= 3.0  # 3x weight for matching hashtags
                
                candidates.append((question_id, weight))
            
            logger.debug(f"Found {len(candidates)} weighted question candidates")
            return candidates
            
        except Exception as e:
            logger.error(f"Failed to get question candidates: {e}")
            return []
    
    @monitor_resources
    def get_user_performance_stats(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive user performance statistics."""
        conn = self.get_connection()  # Get database connection
        
        try:
            # Overall performance stats
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_attempts,
                    SUM(correct) as correct_attempts,
                    AVG(correct) as accuracy,
                    AVG(latency) as avg_latency,
                    MIN(timestamp) as first_attempt,
                    MAX(timestamp) as last_attempt
                FROM attempts WHERE user_id = ?
            """, (user_id,))
            overall_stats = cursor.fetchone()
            
            # Performance by category
            cursor = conn.execute("""
                SELECT 
                    q.categories,
                    COUNT(*) as attempts,
                    SUM(a.correct) as correct,
                    AVG(a.correct) as accuracy,
                    AVG(a.latency) as avg_latency
                FROM attempts a
                JOIN questions q ON a.question_id = q.question_id
                WHERE a.user_id = ?
                GROUP BY q.categories
            """, (user_id,))
            category_stats = cursor.fetchall()
            
            # Recent performance trend (last 30 days)
            cursor = conn.execute("""
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as attempts,
                    SUM(correct) as correct,
                    AVG(correct) as accuracy
                FROM attempts 
                WHERE user_id = ? AND timestamp >= datetime('now', '-30 days')
                GROUP BY DATE(timestamp)
                ORDER BY date
            """, (user_id,))
            trend_stats = cursor.fetchall()
            
            # Compile comprehensive stats
            stats = {
                'user_id': user_id,
                'overall': dict(overall_stats) if overall_stats else {},
                'by_category': [dict(row) for row in category_stats],
                'trend': [dict(row) for row in trend_stats],
                'generated_at': datetime.now().isoformat()
            }
            
            logger.debug(f"Generated performance stats for user {user_id}")
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get user performance stats: {e}")
            return {'user_id': user_id, 'error': str(e)}


# Global database instance for easy access
_quiz_db: Optional[QuizDatabase] = None
_db_lock = threading.Lock()


def get_quiz_database(db_path: str = "quiz-app/data/db/quiz.sqlite") -> QuizDatabase:
    """Get global quiz database instance."""
    global _quiz_db
    
    with _db_lock:
        if _quiz_db is None:
            _quiz_db = QuizDatabase(db_path)
            _quiz_db.initialize({})  # Initialize with empty config
        return _quiz_db