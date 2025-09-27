# src/quiz_dashboard/spaced_repetition.py

"""
Spaced Repetition (SM-2) Algorithm Implementation for Quiz Dashboard.

This module implements the SuperMemo-2 algorithm with custom enhancements for
adaptive learning and optimal question scheduling. Features include:

- Classic SM-2 algorithm with configurable parameters
- Adaptive difficulty adjustment based on performance patterns  
- Anti-clustering to prevent similar questions appearing consecutively
- Performance analytics and learning curve tracking
- Weighted question selection with multiple factors
- Custom scheduling for different learning objectives
"""

import math
import random
import threading
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics

# Import Framework0 components
from src.core.logger import get_logger
from .models import QuizDatabase, get_quiz_database

# Initialize module logger
logger = get_logger(__name__)


class PerformanceLevel(Enum):
    """Performance levels for SM-2 algorithm scoring."""
    BLACKOUT = 0      # Complete failure (0-1)
    INCORRECT = 1     # Incorrect response (2)  
    DIFFICULT = 2     # Correct with difficulty (3)
    EASY = 3          # Correct response (4)
    PERFECT = 4       # Perfect response (5)


@dataclass
class SM2Parameters:
    """Configuration parameters for SM-2 algorithm."""
    initial_easiness: float = 2.5      # Initial easiness factor
    min_easiness: float = 1.3          # Minimum easiness factor  
    max_easiness: float = 4.0          # Maximum easiness factor
    easiness_increment: float = 0.1    # Increment for good responses
    easiness_decrement: float = 0.8    # Decrement for poor responses
    min_interval: int = 1              # Minimum interval (days)
    max_interval: int = 365            # Maximum interval (days)
    initial_interval: int = 1          # Initial interval for new questions
    second_interval: int = 6           # Second interval for questions
    performance_threshold: float = 3.0 # Threshold for successful recall


@dataclass  
class QuestionProgress:
    """Progress tracking data for individual questions."""
    question_id: int                           # Question database ID
    user_id: int                              # User database ID  
    easiness_factor: float = 2.5              # Current easiness factor
    repetition_count: int = 0                 # Number of repetitions
    interval_days: int = 1                    # Current interval in days
    next_review_date: Optional[date] = None   # Next scheduled review
    last_reviewed: Optional[datetime] = None  # Last review timestamp
    total_attempts: int = 0                   # Total attempt count
    correct_attempts: int = 0                 # Successful attempts
    average_time: float = 0.0                 # Average response time
    current_difficulty: int = 3               # Current difficulty level
    mastery_level: float = 0.0                # Computed mastery score
    performance_history: List[float] = field(default_factory=list)  # Recent performance


@dataclass
class SelectionWeights:
    """Weights for multi-factor question selection algorithm."""
    due_date_weight: float = 0.4       # Weight for due date proximity
    performance_weight: float = 0.25   # Weight for poor performance
    recency_weight: float = 0.15       # Weight for recent attempts
    difficulty_weight: float = 0.1     # Weight for difficulty matching
    hashtag_weight: float = 0.05       # Weight for hashtag preferences  
    randomness_weight: float = 0.05    # Weight for randomness


class SpacedRepetitionEngine:
    """
    Advanced Spaced Repetition engine with SM-2 algorithm.
    
    Implements SuperMemo-2 with enhancements for adaptive learning,
    anti-clustering, and performance analytics. Manages optimal
    question scheduling and difficulty adjustment.
    """
    
    def __init__(self, database: Optional[QuizDatabase] = None,
                 sm2_params: Optional[SM2Parameters] = None,
                 selection_weights: Optional[SelectionWeights] = None) -> None:
        # Execute __init__ operation
        """Initialize spaced repetition system with database and parameters."""
        self.database = database or get_quiz_database()  # Database connection
        self.sm2_params = sm2_params or SM2Parameters()  # SM-2 parameters
        self.selection_weights = selection_weights or SelectionWeights()  # Selection weights
        
        # Anti-clustering state
        self._recent_questions: List[int] = []  # Recently shown question IDs
        self._recent_hashtags: List[str] = []   # Recently shown hashtags
        self._clustering_window = 5             # Questions to avoid clustering
        
        logger.info("SpacedRepetitionEngine initialized with SM-2 algorithm")
    
    def process_question_attempt(self,
                                user_id: int,
                                question_id: int,
                                performance_score: float,
                                time_taken_seconds: float,
                                is_correct: bool) -> QuestionProgress:
        # Execute process_question_attempt operation
        """Process a question attempt and update spaced repetition data."""
        try:
            # Get current progress or create new
            progress = self._get_question_progress(user_id, question_id)
            if not progress:
                progress = QuestionProgress(
                    question_id=question_id,
                    user_id=user_id,
                    next_review_date=date.today()
                )
            
            # Update attempt statistics
            progress.total_attempts += 1
            if is_correct:
                progress.correct_attempts += 1
            
            # Update average time (exponential moving average)
            if progress.average_time == 0:
                progress.average_time = time_taken_seconds
            else:
                progress.average_time = (progress.average_time * 0.8) + (time_taken_seconds * 0.2)
            
            # Update performance history
            progress.performance_history.append(performance_score)
            if len(progress.performance_history) > 10:
                progress.performance_history = progress.performance_history[-10:]
            
            # Apply SM-2 algorithm
            progress = self._apply_sm2_algorithm(progress, performance_score)
            
            # Update mastery level
            progress.mastery_level = self._calculate_mastery_level(progress)
            
            # Save progress to database
            self._save_question_progress(progress)
            
            # Update last reviewed timestamp
            progress.last_reviewed = datetime.now()
            
            logger.debug(f"Question attempt processed: User {user_id}, Question {question_id}, "
                        f"Performance {performance_score}, Next review: {progress.next_review_date}")
            
            return progress
            
        except Exception as e:
            logger.error(f"Failed to process question attempt: {e}")
            raise
    
    def _apply_sm2_algorithm(self, progress: QuestionProgress, performance_score: float) -> QuestionProgress:
        # Execute _apply_sm2_algorithm operation
        """Apply SM-2 spaced repetition algorithm to update question progress."""
        # Convert performance score to SM-2 quality scale (0-5)
        quality = min(5, max(0, int(performance_score)))
        
        # Update easiness factor based on performance
        if quality >= 3:
            # Good performance - increase easiness
            progress.easiness_factor += (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        else:
            # Poor performance - reset to beginning with decreased easiness
            progress.easiness_factor = max(
                self.sm2_params.min_easiness,
                progress.easiness_factor - self.sm2_params.easiness_decrement
            )
            progress.repetition_count = 0
            progress.interval_days = 1
        
        # Clamp easiness factor to valid range
        progress.easiness_factor = max(self.sm2_params.min_easiness,
                                     min(self.sm2_params.max_easiness, progress.easiness_factor))
        
        # Calculate new interval based on repetition count
        if quality < 3:
            # Poor performance - restart
            progress.interval_days = self.sm2_params.initial_interval
            progress.repetition_count = 0
        else:
            # Good performance - advance
            progress.repetition_count += 1
            
            if progress.repetition_count == 1:
                progress.interval_days = self.sm2_params.initial_interval
            elif progress.repetition_count == 2:  
                progress.interval_days = self.sm2_params.second_interval
            else:
                # Use SM-2 formula for subsequent intervals
                progress.interval_days = int(
                    progress.interval_days * progress.easiness_factor
                )
        
        # Apply interval constraints
        progress.interval_days = max(self.sm2_params.min_interval,
                                   min(self.sm2_params.max_interval, progress.interval_days))
        
        # Set next review date
        progress.next_review_date = date.today() + timedelta(days=progress.interval_days)
        
        return progress
    
    def _calculate_mastery_level(self, progress: QuestionProgress) -> float:
        # Execute _calculate_mastery_level operation
        """Calculate mastery level based on progress data."""
        if progress.total_attempts == 0:
            return 0.0
        
        # Base mastery from success rate
        success_rate = progress.correct_attempts / progress.total_attempts
        base_mastery = success_rate * 100
        
        # Adjust based on recent performance
        if progress.performance_history:
            recent_avg = statistics.mean(progress.performance_history)
            recent_factor = recent_avg / 5.0  # Normalize to 0-1
            base_mastery = (base_mastery * 0.7) + (recent_factor * 100 * 0.3)
        
        # Adjust based on consistency (low variance is better)
        if len(progress.performance_history) > 3:
            variance = statistics.variance(progress.performance_history)
            consistency_factor = max(0, 1 - (variance / 5.0))
            base_mastery *= (0.8 + 0.2 * consistency_factor)
        
        # Adjust based on repetition count (more repetitions = higher confidence)
        repetition_factor = min(1.0, progress.repetition_count / 5.0)
        base_mastery *= (0.9 + 0.1 * repetition_factor)
        
        return max(0.0, min(100.0, base_mastery))
    
    def select_next_questions(self,
                             user_id: int,
                             count: int = 10,
                             preferred_hashtags: Optional[List[str]] = None,
                             target_difficulty: Optional[int] = None,
                             avoid_recent: bool = True) -> List[int]:
        # Execute select_next_questions operation
        """Select next questions for user based on spaced repetition algorithm."""
        try:
            # Get available questions with user progress
            candidate_questions = self._get_candidate_questions(user_id, preferred_hashtags, target_difficulty)
            
            if not candidate_questions:
                logger.warning(f"No candidate questions found for user {user_id}")
                return []
            
            # Apply anti-clustering filter
            if avoid_recent:
                candidate_questions = self._filter_recent_questions(candidate_questions)
            
            # Calculate selection scores
            scored_questions = []
            for question_data in candidate_questions:
                score = self._calculate_selection_score(question_data, preferred_hashtags, target_difficulty)
                scored_questions.append((question_data["question_id"], score))
            
            # Sort by score (descending) and select top candidates
            scored_questions.sort(key=lambda x: x[1], reverse=True)
            
            # Add some randomness to avoid predictable patterns
            selection_pool_size = min(count * 3, len(scored_questions))
            selection_pool = scored_questions[:selection_pool_size]
            
            # Select questions with weighted randomness
            selected_questions = []
            weights = [score for _, score in selection_pool]
            
            for _ in range(min(count, len(selection_pool))):
                if not selection_pool:
                    break
                
                # Weighted random selection
                selected_idx = self._weighted_random_choice(weights)
                question_id, _ = selection_pool.pop(selected_idx)
                weights.pop(selected_idx)
                
                selected_questions.append(question_id)
            
            # Update anti-clustering state
            self._update_recent_questions(selected_questions)
            
            logger.info(f"Selected {len(selected_questions)} questions for user {user_id}")
            return selected_questions
            
        except Exception as e:
            logger.error(f"Failed to select next questions: {e}")
            return []
    
    def _get_candidate_questions(self, 
        # _get_candidate_questions operation implementation
                               user_id: int,                               preferred_hashtags: Optional[List[str]] = None,
                               target_difficulty: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            # Build query with filters

            base_query = """
                SELECT 
                    q.id as question_id,
                    q.question_type,
                    q.difficulty_level,
                    q.hashtags,
                    q.estimated_time_seconds,
                    up.easiness_factor,
                    up.next_review_date,
                    up.total_attempts,
                    up.correct_attempts,
                    up.mastery_level,
                    up.last_reviewed_at,
                    COALESCE(up.next_review_date, date('now')) as review_date
                FROM questions q
                LEFT JOIN user_progress up ON q.id = up.question_id AND up.user_id = ?
                WHERE q.is_active = 1"""
            
            params = [user_id]
            conditions = []
            
            # Filter by difficulty if specified
            if target_difficulty is not None:
                conditions.append("q.difficulty_level = ?")
                params.append(target_difficulty)
            
            # Filter by hashtags if specified
            if preferred_hashtags:
                hashtag_conditions = []
                for tag in preferred_hashtags:
                    hashtag_conditions.append("q.hashtags LIKE ?")
                    params.append(f"%\"{tag}\"%")
                conditions.append(f"({' OR '.join(hashtag_conditions)})")
            
            # Apply conditions
            if conditions:
                base_query += " AND " + " AND ".join(conditions)
            
            # Order by review priority
            base_query += """ ORDER BY 
                    CASE 
                        WHEN up.next_review_date <= date('now') THEN 0
                        ELSE 1
                    END,
                    review_date ASC,
                    RANDOM()
                LIMIT 100"""
            
            results = self.database.execute_query(base_query, tuple(params))
            
            candidates = []
            for row in results:
                candidate = {
                    "question_id": row["question_id"],
                    "question_type": row["question_type"], 
                    "difficulty_level": row["difficulty_level"],
                    "hashtags": json.loads(row["hashtags"]) if row["hashtags"] else [],
                    "estimated_time": row["estimated_time_seconds"],
                    "easiness_factor": row["easiness_factor"] or self.sm2_params.initial_easiness,
                    "next_review_date": row["next_review_date"],
                    "total_attempts": row["total_attempts"] or 0,
                    "correct_attempts": row["correct_attempts"] or 0,
                    "mastery_level": row["mastery_level"] or 0.0,
                    "last_reviewed": row["last_reviewed_at"],
                    "due_days": self._calculate_due_days(row["review_date"])
                }
                candidates.append(candidate)
            
            logger.debug(f"Found {len(candidates)} candidate questions")
            return candidates
            
        except Exception as e:
            logger.error(f"Failed to get candidate questions: {e}")
            return []
    
    def _calculate_due_days(self, review_date_str: str) -> int:
        # Execute _calculate_due_days operation
        """Calculate due days from review date string."""
        try:
            review_date = datetime.strptime(review_date_str, "%Y-%m-%d").date()
            today = date.today()
            return (review_date - today).days
        except:
            return 0
    
    def _filter_recent_questions(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Execute _filter_recent_questions operation
        """Filter out recently shown questions."""
        filtered = []
        for candidate in candidates:
            question_id = candidate["question_id"]
            hashtags = candidate["hashtags"]
            
            # Skip if question was recently shown
            if question_id in self._recent_questions:
                continue
            
            # Skip if similar hashtags were recently shown
            if any(tag in self._recent_hashtags for tag in hashtags):
                continue
            
            filtered.append(candidate)
        
        logger.debug(f"Anti-clustering filter: {len(candidates)} -> {len(filtered)} questions")
        return filtered
    
    def _calculate_selection_score(self, 
        # _calculate_selection_score operation implementation
                                 question_data: Dict[str, Any],                                 preferred_hashtags: Optional[List[str]] = None,
                                 target_difficulty: Optional[int] = None) -> float:
        weights = self.selection_weights
        score = 0.0
        
        # Due date factor (higher score for overdue questions)
        due_days = question_data["due_days"]
        if due_days <= 0:
            due_score = 1.0 + abs(due_days) * 0.1  # Bonus for overdue
        else:
            due_score = max(0.1, 1.0 - due_days * 0.05)  # Penalty for future
        score += due_score * weights.due_date_weight
        
        # Performance factor (higher score for poor performance)
        mastery_level = question_data["mastery_level"]
        performance_score = max(0.1, 1.0 - mastery_level / 100.0)
        score += performance_score * weights.performance_weight
        
        # Recency factor (higher score for questions not attempted recently)
        if question_data["last_reviewed"]:
            try:
                last_reviewed = datetime.fromisoformat(question_data["last_reviewed"])
                days_since = (datetime.now() - last_reviewed).days
                recency_score = min(1.0, days_since / 30.0)  # Max score after 30 days
            except:
                recency_score = 1.0
        else:
            recency_score = 1.0  # New questions get full score
        score += recency_score * weights.recency_weight
        
        # Difficulty matching factor
        if target_difficulty is not None:
            difficulty_diff = abs(question_data["difficulty_level"] - target_difficulty)
            difficulty_score = max(0.1, 1.0 - difficulty_diff * 0.2)
        else:
            difficulty_score = 0.5  # Neutral score
        score += difficulty_score * weights.difficulty_weight
        
        # Hashtag preference factor
        if preferred_hashtags:
            question_hashtags = set(question_data["hashtags"])
            preferred_set = set(preferred_hashtags)
            overlap = len(question_hashtags & preferred_set)
            hashtag_score = overlap / len(preferred_set) if preferred_set else 0.0
        else:
            hashtag_score = 0.5  # Neutral score
        score += hashtag_score * weights.hashtag_weight
        
        # Randomness factor
        randomness_score = random.random()
        score += randomness_score * weights.randomness_weight
        
        return max(0.0, score)
    
    def _weighted_random_choice(self, weights: List[float]) -> int:
        # Execute _weighted_random_choice operation
        """Weighted random choice from list based on weights."""
        if not weights:
            return 0
        
        total = sum(weights)
        if total <= 0:
            return random.randint(0, len(weights) - 1)
        
        r = random.uniform(0, total)
        cumulative = 0
        
        for i, weight in enumerate(weights):
            cumulative += weight
            if r <= cumulative:
                return i
        
        return len(weights) - 1
    
    def _update_recent_questions(self, question_ids: List[int]) -> None:
        # Execute _update_recent_questions operation
        # Add new question IDs
        self._recent_questions.extend(question_ids)
        
        # Trim to window size
        if len(self._recent_questions) > self._clustering_window:
            self._recent_questions = self._recent_questions[-self._clustering_window:]
        
        # Update recent hashtags
        try:
            if question_ids:
                placeholders = ",".join("?" * len(question_ids))
                query = f"SELECT hashtags FROM questions WHERE id IN ({placeholders})"
                results = self.database.execute_query(query, tuple(question_ids))
                
                new_hashtags = []
                for row in results:
                    if row["hashtags"]:
                        hashtags = json.loads(row["hashtags"])
                        new_hashtags.extend(hashtags)
                
                self._recent_hashtags.extend(new_hashtags)
                
                # Trim hashtags list
                if len(self._recent_hashtags) > self._clustering_window * 3:
                    self._recent_hashtags = self._recent_hashtags[-self._clustering_window * 3:]
                    
        except Exception as e:
            logger.warning(f"Failed to update recent hashtags: {e}")
    
        def _get_question_progress(self, user_id: int, question_id: int) -> Optional[QuestionProgress]:
        # Execute _get_question_progress operation
        try:
                SELECT user_id, question_id, easiness_factor, repetition_count,
                       interval_days, next_review_date, last_reviewed_at,
                       total_attempts, correct_attempts, average_time_seconds,
                       current_difficulty, mastery_level
                FROM user_progress
                WHERE user_id = ? AND question_id = ?
            
            results = self.database.execute_query(query, (user_id, question_id))
            
            if not results:
                return None
            
            row = results[0]
            
            progress = QuestionProgress(
                question_id=row["question_id"],
                user_id=row["user_id"],
                easiness_factor=row["easiness_factor"],
                repetition_count=row["repetition_count"],
                interval_days=row["interval_days"],
                next_review_date=datetime.strptime(row["next_review_date"], "%Y-%m-%d").date() 
                    if row["next_review_date"] else None,
                last_reviewed=datetime.fromisoformat(row["last_reviewed_at"])
                    if row["last_reviewed_at"] else None,
                total_attempts=row["total_attempts"],
                correct_attempts=row["correct_attempts"],
                average_time=row["average_time_seconds"],
                current_difficulty=row["current_difficulty"],
                mastery_level=row["mastery_level"]
            )
            
            return progress
            
        except Exception as e:
            logger.error(f"Failed to get question progress: {e}")
            return None
    
        def _save_question_progress(self, progress: QuestionProgress) -> None:
        # Execute _save_question_progress operation
        try:
                INSERT OR REPLACE INTO user_progress (
                    user_id, question_id, easiness_factor, repetition_count,
                    interval_days, next_review_date, last_reviewed_at,
                    total_attempts, correct_attempts, average_time_seconds,
                    current_difficulty, mastery_level, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            
            params = (
                progress.user_id,
                progress.question_id,
                progress.easiness_factor,
                progress.repetition_count,
                progress.interval_days,
                progress.next_review_date.isoformat() if progress.next_review_date else None,
                progress.last_reviewed.isoformat() if progress.last_reviewed else None,
                progress.total_attempts,
                progress.correct_attempts,
                progress.average_time,
                progress.current_difficulty,
                progress.mastery_level,
                datetime.now().isoformat()
            )
            
            self.database.execute_update(query, params)
            
        except Exception as e:
            logger.error(f"Failed to save question progress: {e}")
            raise
    
        def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        # Execute get_user_statistics operation
        try:
            # Basic progress statistics
                SELECT 
                    COUNT(*) as total_questions_attempted,
                    COUNT(CASE WHEN mastery_level >= 80 THEN 1 END) as mastered_questions,
                    AVG(mastery_level) as average_mastery,
                    COUNT(CASE WHEN next_review_date <= date('now') THEN 1 END) as due_for_review,
                    AVG(correct_attempts * 1.0 / total_attempts) as overall_accuracy
                FROM user_progress 
                WHERE user_id = ? AND total_attempts > 0
            
            stats_results = self.database.execute_query(stats_query, (user_id,))
            stats_row = stats_results[0] if stats_results else {}
            
            # Learning streak calculation
                SELECT COUNT(*) as current_streak
                FROM performance_analytics
                WHERE user_id = ? 
                  AND analytics_date >= date('now', '-30 days')
                  AND questions_attempted > 0
                ORDER BY analytics_date DESC
            
            streak_results = self.database.execute_query(streak_query, (user_id,))
            current_streak = streak_results[0]["current_streak"] if streak_results else 0
            
            # Difficulty distribution
                SELECT 
                    q.difficulty_level,
                    COUNT(*) as count,
                    AVG(up.mastery_level) as avg_mastery
                FROM user_progress up
                JOIN questions q ON up.question_id = q.id
                WHERE up.user_id = ? AND up.total_attempts > 0
                GROUP BY q.difficulty_level
                ORDER BY q.difficulty_level
            
            difficulty_results = self.database.execute_query(difficulty_query, (user_id,))
            difficulty_distribution = {
                row["difficulty_level"]: {
                    "count": row["count"],
                    "avg_mastery": row["avg_mastery"]
                } for row in difficulty_results
            }
            
            statistics = {
                "user_id": user_id,
                "total_questions_attempted": stats_row.get("total_questions_attempted", 0),
                "mastered_questions": stats_row.get("mastered_questions", 0),
                "average_mastery": round(stats_row.get("average_mastery", 0.0), 2),
                "due_for_review": stats_row.get("due_for_review", 0),
                "overall_accuracy": round(stats_row.get("overall_accuracy", 0.0), 3),
                "current_learning_streak": current_streak,
                "difficulty_distribution": difficulty_distribution,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.debug(f"Generated user statistics for user {user_id}")
            return statistics
            
        except Exception as e:
            logger.error(f"Failed to get user statistics: {e}")
            return {"user_id": user_id, "error": str(e)}


        # Global spaced repetition engine instance
        _sr_engine: Optional[SpacedRepetitionEngine] = None
        _engine_lock = threading.Lock()


        def get_spaced_repetition_engine(database: Optional[QuizDatabase] = None) -> SpacedRepetitionEngine:
        # Execute get_spaced_repetition_engine operation
        global _sr_engine
    
        with _engine_lock:
        if _sr_engine is None:
            _sr_engine = SpacedRepetitionEngine(database)
    
        return _sr_engine


        # Import json for hashtag parsing
        import json
        import threading