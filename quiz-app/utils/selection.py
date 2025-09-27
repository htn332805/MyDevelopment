# quiz-app/utils/selection.py

"""
Advanced question selection and spaced-repetition algorithm for quiz application.

This module implements intelligent question selection including:
- SM-2 inspired spaced repetition algorithm
- Adaptive difficulty adjustment based on user performance
- Weighted random sampling with performance bias
- Category and hashtag-based filtering and boosting
- Anti-clustering to prevent similar questions in sequence
- Learning curve optimization and retention prediction

Integrates with Framework0's analytics and performance monitoring.
"""

import random
import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set, NamedTuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics

# Import Framework0 components
from src.core.logger import get_logger
from src.core.interfaces import ComponentLifecycle, Configurable
from src.core.decorators_v2 import monitor_resources, debug_trace
from src.core.error_handling import handle_errors, ErrorCategory

# Import quiz components
sys.path.append("..")  # Add parent directory for imports
from models.storage import get_quiz_database, QuizDatabase, QuestionStats
from utils.qloader import get_question_loader, QuestionLoader

# Initialize logger with debug support
logger = get_logger(__name__, debug=True)


@dataclass
class SelectionCriteria:
    """Criteria for question selection."""
    user_id: int  # User making the selection
    num_questions: int = 10  # Number of questions to select
    categories: Optional[List[str]] = None  # Filter by categories
    hashtags: Optional[List[str]] = None  # Filter by hashtags
    difficulty: Optional[str] = None  # Filter by difficulty
    question_types: Optional[List[str]] = None  # Filter by question types
    avoid_recent: bool = True  # Avoid recently seen questions
    recent_window_hours: int = 24  # Hours to consider as "recent"
    prioritize_due: bool = True  # Prioritize SM-2 due questions
    due_percentage: float = 0.4  # % of questions that should be due
    balance_types: bool = True  # Balance different question types
    anti_cluster: bool = True  # Prevent clustering of similar questions
    adaptive_difficulty: bool = True  # Adjust difficulty based on performance


@dataclass
class QuestionCandidate:
    """Question candidate with selection metadata."""
    question_id: str  # Question identifier
    question_data: Dict[str, Any]  # Full question data
    base_weight: float  # Base selection weight
    performance_weight: float  # Performance-based weight multiplier
    recency_weight: float  # Recency-based weight multiplier
    hashtag_weight: float  # Hashtag-based weight multiplier
    difficulty_weight: float  # Difficulty-based weight multiplier
    due_weight: float  # SM-2 due weight multiplier
    final_weight: float  # Final computed weight
    stats: QuestionStats  # Question statistics
    is_due: bool = False  # Whether question is due for review
    days_since_seen: int = 0  # Days since last seen
    predicted_difficulty: float = 0.5  # Predicted difficulty for user (0-1)


class SpacedRepetitionSelector(ComponentLifecycle, Configurable):
    """
    Advanced question selector with spaced repetition and adaptive algorithms.
    
    Implements intelligent question selection that adapts to user performance,
    optimizes learning efficiency, and maintains engagement through variety.
    """
    
    def __init__(self):
        """Initialize spaced repetition selector."""
        super().__init__()
        self.db: Optional[QuizDatabase] = None  # Database interface
        self.loader: Optional[QuestionLoader] = None  # Question loader
        self.user_profiles = {}  # Cached user performance profiles
        self.selection_history = defaultdict(deque)  # Recent selection history per user
        self.performance_cache = {}  # Cached performance calculations
        
        # Algorithm parameters (tunable)
        self.params = {
            'base_difficulty_weights': {'easy': 1.0, 'medium': 2.0, 'hard': 3.0},
            'error_multiplier': 2.0,  # Weight multiplier for incorrect answers
            'recent_miss_boost': 2.0,  # Boost for recently missed questions
            'hashtag_boost': 3.0,  # Boost for matching hashtags
            'due_boost': 2.0,  # Boost for SM-2 due questions
            'variety_penalty': 0.8,  # Penalty for recently selected questions
            'min_weight': 0.1,  # Minimum question weight
            'max_weight': 10.0,  # Maximum question weight
            'clustering_penalty': 0.5,  # Penalty for clustering similar questions
            'adaptive_difficulty_factor': 0.3,  # How much to adjust difficulty
        }
        
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Initialize selector with database and loader connections."""
        logger.info("Initializing spaced repetition selector")
        
        # Connect to database and loader
        self.db = get_quiz_database()
        self.loader = get_question_loader()
        
        # Update parameters from config
        if 'selection_params' in config:
            self.params.update(config['selection_params'])
        
        logger.info("Spaced repetition selector initialized")
        
    def _do_cleanup(self) -> None:
        """Clean up selector resources."""
        logger.info("Cleaning up spaced repetition selector")
        
        # Clear caches
        self.user_profiles.clear()
        self.selection_history.clear()
        self.performance_cache.clear()
        
        logger.info("Spaced repetition selector cleanup completed")
    
    @monitor_resources
    @debug_trace
    def select_questions(self, criteria: SelectionCriteria) -> List[Dict[str, Any]]:
        """Select questions using advanced spaced repetition algorithm."""
        logger.info(f"Selecting {criteria.num_questions} questions for user {criteria.user_id}")
        
        try:
            # Get user performance profile
            user_profile = self._get_user_profile(criteria.user_id)
            
            # Get question candidates
            candidates = self._get_question_candidates(criteria, user_profile)
            
            if not candidates:
                logger.warning("No question candidates found")
                return []
            
            # Apply selection algorithm
            selected = self._apply_selection_algorithm(candidates, criteria, user_profile)
            
            # Update selection history
            self._update_selection_history(criteria.user_id, selected)
            
            # Return question data
            questions = [candidate.question_data for candidate in selected]
            
            logger.info(f"Selected {len(questions)} questions successfully")
            return questions
            
        except Exception as e:
            logger.error(f"Failed to select questions: {e}")
            with handle_errors(ErrorCategory.PROCESSING):
                raise
    
    def _get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get or create user performance profile."""
        if user_id in self.user_profiles:
            profile = self.user_profiles[user_id]
            
            # Refresh if old
            if (datetime.now() - profile['last_updated']).seconds > 3600:  # 1 hour
                profile = self._build_user_profile(user_id)
                self.user_profiles[user_id] = profile
        else:
            profile = self._build_user_profile(user_id)
            self.user_profiles[user_id] = profile
        
        return profile
    
    def _build_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Build comprehensive user performance profile."""
        logger.debug(f"Building performance profile for user {user_id}")
        
        try:
            # Get user performance stats from database
            stats = self.db.get_user_performance_stats(user_id)
            
            # Extract key metrics
            overall = stats.get('overall', {})
            total_attempts = overall.get('total_attempts', 0)
            accuracy = overall.get('accuracy', 0.5)
            avg_latency = overall.get('avg_latency', 30.0)
            
            # Calculate adaptive difficulty level
            if accuracy >= 0.8:
                preferred_difficulty = 'hard'
                difficulty_bias = 1.2
            elif accuracy >= 0.6:
                preferred_difficulty = 'medium'
                difficulty_bias = 1.0
            else:
                preferred_difficulty = 'easy'
                difficulty_bias = 0.8
            
            # Analyze category performance
            category_performance = {}
            for cat_stat in stats.get('by_category', []):
                if cat_stat.get('categories'):
                    try:
                        categories = eval(cat_stat['categories'])  # Parse JSON-like string
                        for category in categories:
                            category_performance[category] = {
                                'accuracy': cat_stat.get('accuracy', 0.5),
                                'attempts': cat_stat.get('attempts', 0),
                                'avg_latency': cat_stat.get('avg_latency', 30.0)
                            }
                    except:
                        pass  # Skip invalid category data
            
            # Calculate learning velocity (improvement over time)
            trend_data = stats.get('trend', [])
            learning_velocity = 0.0
            if len(trend_data) >= 2:
                recent_accuracy = statistics.mean([t.get('accuracy', 0.5) for t in trend_data[-7:]])
                older_accuracy = statistics.mean([t.get('accuracy', 0.5) for t in trend_data[-14:-7]])
                learning_velocity = recent_accuracy - older_accuracy
            
            profile = {
                'user_id': user_id,
                'total_attempts': total_attempts,
                'overall_accuracy': accuracy,
                'avg_latency': avg_latency,
                'preferred_difficulty': preferred_difficulty,
                'difficulty_bias': difficulty_bias,
                'category_performance': category_performance,
                'learning_velocity': learning_velocity,
                'experience_level': 'beginner' if total_attempts < 50 else 
                                  'intermediate' if total_attempts < 200 else 'advanced',
                'last_updated': datetime.now(),
                'stats': stats
            }
            
            logger.debug(f"Built profile for user {user_id}: {profile['experience_level']} level, "
                        f"{profile['overall_accuracy']:.1%} accuracy")
            
            return profile
            
        except Exception as e:
            logger.error(f"Failed to build user profile: {e}")
            # Return default profile
            return {
                'user_id': user_id,
                'total_attempts': 0,
                'overall_accuracy': 0.5,
                'avg_latency': 30.0,
                'preferred_difficulty': 'medium',
                'difficulty_bias': 1.0,
                'category_performance': {},
                'learning_velocity': 0.0,
                'experience_level': 'beginner',
                'last_updated': datetime.now(),
                'stats': {}
            }
    
    @monitor_resources
    def _get_question_candidates(self, criteria: SelectionCriteria, 
                               user_profile: Dict[str, Any]) -> List[QuestionCandidate]:
        """Get and evaluate question candidates."""
        logger.debug("Getting question candidates")
        
        # Get filtered questions from loader
        questions = self.loader.get_questions_by_criteria(
            categories=criteria.categories,
            question_type=criteria.question_types[0] if criteria.question_types and len(criteria.question_types) == 1 else None,
            difficulty=criteria.difficulty
        )
        
        # Get weighted candidates from database
        db_candidates = self.db.get_weighted_question_candidates(
            criteria.user_id,
            categories=criteria.categories,
            hashtags=criteria.hashtags,
            limit=len(questions) * 2  # Get more candidates for better selection
        )
        
        # Combine and evaluate candidates
        candidates = []
        recent_questions = set(self._get_recent_questions(criteria.user_id, criteria.recent_window_hours))
        
        for question in questions:
            question_id = str(question['question_id'])
            
            # Skip recently seen questions if requested
            if criteria.avoid_recent and question_id in recent_questions:
                continue
            
            # Get question statistics
            stats = self.db.get_question_stats(question_id)
            
            # Calculate candidate weights
            candidate = self._evaluate_candidate(
                question, stats, criteria, user_profile, db_candidates
            )
            
            candidates.append(candidate)
        
        # Sort by final weight
        candidates.sort(key=lambda c: c.final_weight, reverse=True)
        
        logger.debug(f"Evaluated {len(candidates)} question candidates")
        return candidates
    
    def _evaluate_candidate(self, question: Dict[str, Any], stats: QuestionStats,
                           criteria: SelectionCriteria, user_profile: Dict[str, Any],
                           db_candidates: List[Tuple[str, float]]) -> QuestionCandidate:
        """Evaluate a single question candidate."""
        question_id = str(question['question_id'])
        
        # Get base weight from database
        base_weight = next((weight for qid, weight in db_candidates if qid == question_id), 1.0)
        
        # Calculate performance weight
        performance_weight = self._calculate_performance_weight(stats, user_profile)
        
        # Calculate recency weight
        recency_weight = self._calculate_recency_weight(stats, criteria)
        
        # Calculate hashtag weight
        hashtag_weight = self._calculate_hashtag_weight(question, criteria)
        
        # Calculate difficulty weight
        difficulty_weight = self._calculate_difficulty_weight(question, user_profile, criteria)
        
        # Calculate SM-2 due weight
        due_weight, is_due = self._calculate_due_weight(stats, criteria)
        
        # Calculate days since seen
        days_since_seen = 0
        if stats.last_seen:
            days_since_seen = (datetime.now() - stats.last_seen).days
        
        # Calculate predicted difficulty
        predicted_difficulty = self._predict_difficulty(question, user_profile)
        
        # Combine all weights
        final_weight = (base_weight * performance_weight * recency_weight * 
                       hashtag_weight * difficulty_weight * due_weight)
        
        # Apply bounds
        final_weight = max(self.params['min_weight'], 
                          min(self.params['max_weight'], final_weight))
        
        return QuestionCandidate(
            question_id=question_id,
            question_data=question,
            base_weight=base_weight,
            performance_weight=performance_weight,
            recency_weight=recency_weight,
            hashtag_weight=hashtag_weight,
            difficulty_weight=difficulty_weight,
            due_weight=due_weight,
            final_weight=final_weight,
            stats=stats,
            is_due=is_due,
            days_since_seen=days_since_seen,
            predicted_difficulty=predicted_difficulty
        )
    
    def _calculate_performance_weight(self, stats: QuestionStats, user_profile: Dict[str, Any]) -> float:
        """Calculate weight based on question performance."""
        if stats.total_seen == 0:
            return 1.0  # Neutral weight for new questions
        
        # Error rate calculation
        error_rate = (stats.total_seen - stats.total_correct) / stats.total_seen
        
        # Increase weight for questions with high error rates
        error_multiplier = 1.0 + (error_rate * self.params['error_multiplier'])
        
        return error_multiplier
    
    def _calculate_recency_weight(self, stats: QuestionStats, criteria: SelectionCriteria) -> float:
        """Calculate weight based on how recently the question was seen."""
        if not stats.last_seen:
            return 1.0  # Neutral weight for never-seen questions
        
        hours_since_seen = (datetime.now() - stats.last_seen).total_seconds() / 3600
        
        if hours_since_seen < criteria.recent_window_hours:
            # Recently seen - reduce weight
            return self.params['variety_penalty']
        elif hours_since_seen < 168:  # Within a week
            # Was seen recently and got it wrong - boost weight
            if stats.total_seen > stats.total_correct:
                return self.params['recent_miss_boost']
        
        return 1.0  # Neutral weight
    
    def _calculate_hashtag_weight(self, question: Dict[str, Any], criteria: SelectionCriteria) -> float:
        """Calculate weight based on hashtag matching."""
        if not criteria.hashtags:
            return 1.0  # No hashtag filtering
        
        question_hashtags = set(question.get('hashtags', []))
        requested_hashtags = set(criteria.hashtags)
        
        # Boost weight if hashtags match
        if question_hashtags & requested_hashtags:
            return self.params['hashtag_boost']
        
        return 1.0  # Neutral weight
    
    def _calculate_difficulty_weight(self, question: Dict[str, Any], 
                                   user_profile: Dict[str, Any], criteria: SelectionCriteria) -> float:
        """Calculate weight based on question difficulty vs user capability."""
        question_difficulty = question.get('difficulty', 'medium')
        user_bias = user_profile['difficulty_bias']
        
        # Map difficulty to numeric values
        difficulty_values = {'easy': 1, 'medium': 2, 'hard': 3}
        q_value = difficulty_values[question_difficulty]
        
        # Adjust based on user's preferred difficulty
        preferred_value = difficulty_values.get(user_profile['preferred_difficulty'], 2)
        
        # Calculate adaptive weight
        if criteria.adaptive_difficulty:
            difficulty_delta = abs(q_value - preferred_value)
            if difficulty_delta == 0:
                return 1.2  # Slight boost for optimal difficulty
            elif difficulty_delta == 1:
                return 1.0  # Neutral for slightly off
            else:
                return 0.8  # Slight penalty for very different difficulty
        
        return user_bias
    
    def _calculate_due_weight(self, stats: QuestionStats, criteria: SelectionCriteria) -> Tuple[float, bool]:
        """Calculate weight based on SM-2 spaced repetition schedule."""
        if not criteria.prioritize_due:
            return 1.0, False
        
        # Check if question is due for review
        if stats.last_correct:
            days_since_correct = (datetime.now() - stats.last_correct).days
            is_due = days_since_correct >= stats.interval
        else:
            is_due = True  # Never answered correctly - always due
        
        if is_due:
            return self.params['due_boost'], True
        
        return 1.0, False
    
    def _predict_difficulty(self, question: Dict[str, Any], user_profile: Dict[str, Any]) -> float:
        """Predict how difficult this question will be for the user."""
        # Base difficulty from question
        difficulty_map = {'easy': 0.3, 'medium': 0.5, 'hard': 0.7}
        base_difficulty = difficulty_map.get(question.get('difficulty', 'medium'), 0.5)
        
        # Adjust based on user's performance in this category
        categories = question.get('categories', [])
        category_adjustment = 0.0
        
        for category in categories:
            if category in user_profile['category_performance']:
                cat_accuracy = user_profile['category_performance'][category]['accuracy']
                # Higher accuracy means lower predicted difficulty
                category_adjustment -= (cat_accuracy - 0.5) * 0.2
        
        if categories:
            category_adjustment /= len(categories)
        
        # Combine base difficulty with category adjustment
        predicted = base_difficulty + category_adjustment
        
        # Bound between 0.1 and 0.9
        return max(0.1, min(0.9, predicted))
    
    @monitor_resources
    def _apply_selection_algorithm(self, candidates: List[QuestionCandidate],
                                 criteria: SelectionCriteria, 
                                 user_profile: Dict[str, Any]) -> List[QuestionCandidate]:
        """Apply selection algorithm to choose final questions."""
        logger.debug(f"Applying selection algorithm to {len(candidates)} candidates")
        
        selected = []
        remaining = candidates.copy()
        
        # Phase 1: Select due questions (if prioritizing due)
        if criteria.prioritize_due:
            due_candidates = [c for c in remaining if c.is_due]
            due_count = min(int(criteria.num_questions * criteria.due_percentage), len(due_candidates))
            
            if due_candidates and due_count > 0:
                due_selected = self._weighted_sample(due_candidates, due_count)
                selected.extend(due_selected)
                remaining = [c for c in remaining if c not in due_selected]
        
        # Phase 2: Fill remaining slots with weighted random selection
        remaining_slots = criteria.num_questions - len(selected)
        if remaining_slots > 0 and remaining:
            additional_selected = self._weighted_sample(remaining, remaining_slots)
            selected.extend(additional_selected)
        
        # Phase 3: Apply anti-clustering if enabled
        if criteria.anti_cluster and len(selected) > 1:
            selected = self._apply_anti_clustering(selected)
        
        # Phase 4: Balance question types if enabled
        if criteria.balance_types:
            selected = self._balance_question_types(selected, criteria.num_questions)
        
        logger.debug(f"Selected {len(selected)} questions after algorithm")
        return selected[:criteria.num_questions]
    
    def _weighted_sample(self, candidates: List[QuestionCandidate], k: int) -> List[QuestionCandidate]:
        """Perform weighted random sampling of candidates."""
        if k >= len(candidates):
            return candidates
        
        # Extract weights
        weights = [c.final_weight for c in candidates]
        total_weight = sum(weights)
        
        if total_weight == 0:
            # Fallback to uniform sampling
            return random.sample(candidates, k)
        
        # Weighted sampling
        selected = []
        candidates_copy = candidates.copy()
        weights_copy = weights.copy()
        
        for _ in range(k):
            if not candidates_copy:
                break
            
            # Choose based on weights
            choice = random.choices(candidates_copy, weights=weights_copy, k=1)[0]
            selected.append(choice)
            
            # Remove selected candidate
            index = candidates_copy.index(choice)
            candidates_copy.pop(index)
            weights_copy.pop(index)
        
        return selected
    
    def _apply_anti_clustering(self, selected: List[QuestionCandidate]) -> List[QuestionCandidate]:
        """Apply anti-clustering to reduce similar questions appearing together."""
        if len(selected) <= 1:
            return selected
        
        # Calculate similarity scores between questions
        similarity_matrix = self._calculate_similarity_matrix(selected)
        
        # Reorder to minimize clustering
        reordered = self._minimize_clustering(selected, similarity_matrix)
        
        logger.debug("Applied anti-clustering to question order")
        return reordered
    
    def _calculate_similarity_matrix(self, candidates: List[QuestionCandidate]) -> List[List[float]]:
        """Calculate similarity scores between question candidates."""
        n = len(candidates)
        matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                similarity = self._calculate_similarity(candidates[i], candidates[j])
                matrix[i][j] = similarity
                matrix[j][i] = similarity
        
        return matrix
    
    def _calculate_similarity(self, candidate1: QuestionCandidate, candidate2: QuestionCandidate) -> float:
        """Calculate similarity score between two question candidates."""
        q1 = candidate1.question_data
        q2 = candidate2.question_data
        
        similarity = 0.0
        
        # Type similarity
        if q1.get('type') == q2.get('type'):
            similarity += 0.3
        
        # Difficulty similarity
        if q1.get('difficulty') == q2.get('difficulty'):
            similarity += 0.2
        
        # Category similarity
        cat1 = set(q1.get('categories', []))
        cat2 = set(q2.get('categories', []))
        if cat1 & cat2:
            similarity += 0.3 * len(cat1 & cat2) / max(len(cat1 | cat2), 1)
        
        # Hashtag similarity
        hash1 = set(q1.get('hashtags', []))
        hash2 = set(q2.get('hashtags', []))
        if hash1 & hash2:
            similarity += 0.2 * len(hash1 & hash2) / max(len(hash1 | hash2), 1)
        
        return similarity
    
    def _minimize_clustering(self, candidates: List[QuestionCandidate], 
                           similarity_matrix: List[List[float]]) -> List[QuestionCandidate]:
        """Minimize clustering using a simple greedy algorithm."""
        if len(candidates) <= 2:
            return candidates
        
        # Start with first question
        result = [candidates[0]]
        remaining = list(range(1, len(candidates)))
        
        while remaining:
            # Find the question most dissimilar to the last selected
            last_idx = candidates.index(result[-1])
            
            best_idx = remaining[0]
            best_similarity = similarity_matrix[last_idx][best_idx]
            
            for idx in remaining[1:]:
                similarity = similarity_matrix[last_idx][idx]
                if similarity < best_similarity:
                    best_similarity = similarity
                    best_idx = idx
            
            result.append(candidates[best_idx])
            remaining.remove(best_idx)
        
        return result
    
    def _balance_question_types(self, selected: List[QuestionCandidate], 
                              target_count: int) -> List[QuestionCandidate]:
        """Balance question types in the selection."""
        # Count current types
        type_counts = defaultdict(int)
        for candidate in selected:
            qtype = candidate.question_data.get('type', 'unknown')
            type_counts[qtype] += 1
        
        # If only one type or already balanced, return as-is
        if len(type_counts) <= 1:
            return selected
        
        # Calculate target distribution (roughly equal)
        types = list(type_counts.keys())
        target_per_type = target_count // len(types)
        
        # Group candidates by type
        by_type = defaultdict(list)
        for candidate in selected:
            qtype = candidate.question_data.get('type', 'unknown')
            by_type[qtype].append(candidate)
        
        # Rebalance
        balanced = []
        for qtype in types:
            candidates_of_type = by_type[qtype]
            take_count = min(target_per_type, len(candidates_of_type))
            # Sort by weight and take the best
            candidates_of_type.sort(key=lambda c: c.final_weight, reverse=True)
            balanced.extend(candidates_of_type[:take_count])
        
        # Fill remaining slots with highest-weighted candidates
        remaining_slots = target_count - len(balanced)
        if remaining_slots > 0:
            remaining_candidates = [c for c in selected if c not in balanced]
            remaining_candidates.sort(key=lambda c: c.final_weight, reverse=True)
            balanced.extend(remaining_candidates[:remaining_slots])
        
        logger.debug(f"Balanced question types: {dict(type_counts)} -> {len(balanced)} total")
        return balanced[:target_count]
    
    def _get_recent_questions(self, user_id: int, hours: int) -> List[str]:
        """Get questions seen by user in the last N hours."""
        # This would query the database for recent attempts
        # Simplified implementation for now
        recent_questions = []
        
        try:
            conn = self.db.get_connection()
            cursor = conn.execute("""
                SELECT DISTINCT question_id 
                FROM attempts 
                WHERE user_id = ? AND timestamp > datetime('now', '-{} hours')
            """.format(hours), (user_id,))
            
            recent_questions = [row['question_id'] for row in cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Failed to get recent questions: {e}")
        
        return recent_questions
    
    def _update_selection_history(self, user_id: int, selected: List[QuestionCandidate]) -> None:
        """Update selection history for user."""
        question_ids = [c.question_id for c in selected]
        
        # Keep last 100 selections per user
        if user_id not in self.selection_history:
            self.selection_history[user_id] = deque(maxlen=100)
        
        self.selection_history[user_id].extend(question_ids)
        
        logger.debug(f"Updated selection history for user {user_id}")
    
    def get_selection_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get analytics about question selection for a user."""
        try:
            user_profile = self._get_user_profile(user_id)
            recent_selections = list(self.selection_history.get(user_id, []))
            
            analytics = {
                'user_profile': user_profile,
                'recent_selections': recent_selections[-20:],  # Last 20 selections
                'selection_params': self.params.copy(),
                'generated_at': datetime.now().isoformat()
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Failed to generate selection analytics: {e}")
            return {'error': str(e)}


# Global selector instance
_selector: Optional[SpacedRepetitionSelector] = None
_selector_lock = threading.Lock()


def get_spaced_repetition_selector() -> SpacedRepetitionSelector:
    """Get global spaced repetition selector instance."""
    global _selector
    
    with _selector_lock:
        if _selector is None:
            _selector = SpacedRepetitionSelector()
            _selector.initialize({})
        return _selector


def select_quiz_questions(user_id: int, num_questions: int = 10,
                         categories: Optional[List[str]] = None,
                         hashtags: Optional[List[str]] = None,
                         difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
    """Convenient function to select quiz questions."""
    selector = get_spaced_repetition_selector()
    
    criteria = SelectionCriteria(
        user_id=user_id,
        num_questions=num_questions,
        categories=categories,
        hashtags=hashtags,
        difficulty=difficulty
    )
    
    return selector.select_questions(criteria)