# src/quiz_dashboard/web_app.py

"""
Flask web application for Quiz Dashboard.

This module provides the complete web interface for the quiz dashboard including:
- Student quiz-taking interface with all question types
- Quiz creation and management interface for instructors  
- Analytics dashboard with progress visualization
- RESTful API for quiz operations
- Responsive Bootstrap UI with mobile support
- MathJax integration for LaTeX mathematical notation
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask import abort, send_from_directory
import sqlite3
import threading

# Import Framework0 components
from src.core.logger import get_logger
from .models import initialize_database, QuizDatabase, QuestionType, QuizSessionStatus
from .question_manager import get_question_manager, QuestionValidationResult
from .spaced_repetition import get_spaced_repetition_engine

# Initialize module logger
logger = get_logger(__name__)


class QuizWebApp:
    """
    Complete Flask web application for Quiz Dashboard.
    
    Provides comprehensive web interface with student and instructor views,
    RESTful API, and responsive UI with advanced quiz functionality.
    """
    
    def __init__(self, database_path: str = "quiz_dashboard.db") -> None:
        # Execute __init__ operation
        """Initialize Flask web application."""
        # Initialize Flask app
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self.app.secret_key = os.urandom(24)  # For session management
        
        # Initialize database and managers
        self.database = initialize_database(database_path)
        self.question_manager = get_question_manager(self.database)
        self.sr_engine = get_spaced_repetition_engine(self.database)
        
        # Configure Flask app
        self.app.config.update(
            DATABASE_PATH=database_path,
            MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
            UPLOAD_EXTENSIONS=['.json'],
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SECURE=False  # Set True for HTTPS
        )
        
        # Register routes
        self._register_routes()
        
        logger.info("QuizWebApp initialized successfully")
    
    def _register_routes(self) -> None:
        # Execute _register_routes operation
        """Register all Flask routes."""
        # Main dashboard routes
        self.app.route('/', methods=['GET'])(self.index)
        self.app.route('/dashboard', methods=['GET'])(self.dashboard)
        self.app.route('/student', methods=['GET'])(self.student_dashboard)
        self.app.route('/instructor', methods=['GET'])(self.instructor_dashboard)
        
        # Quiz session routes
        self.app.route('/quiz/start', methods=['POST'])(self.start_quiz_session)
        self.app.route('/quiz/<session_id>', methods=['GET'])(self.quiz_interface)
        self.app.route('/quiz/<session_id>/question', methods=['GET'])(self.get_next_question)
        self.app.route('/quiz/<session_id>/submit', methods=['POST'])(self.submit_question_answer)
        self.app.route('/quiz/<session_id>/complete', methods=['POST'])(self.complete_quiz_session)
        
        # Question management routes
        self.app.route('/questions', methods=['GET'])(self.list_questions)
        self.app.route('/questions/create', methods=['GET', 'POST'])(self.create_question)
        self.app.route('/questions/<int:question_id>', methods=['GET'])(self.view_question)
        self.app.route('/questions/import', methods=['GET', 'POST'])(self.import_questions)
        
        # Analytics routes
        self.app.route('/analytics', methods=['GET'])(self.analytics_dashboard)
        self.app.route('/analytics/user/<int:user_id>', methods=['GET'])(self.user_analytics)
        
        # API routes
        self.app.route('/api/questions/search', methods=['GET'])(self.api_search_questions)
        self.app.route('/api/questions/validate', methods=['POST'])(self.api_validate_question)
        self.app.route('/api/user/<int:user_id>/progress', methods=['GET'])(self.api_user_progress)
        self.app.route('/api/quiz/recommendations/<int:user_id>', methods=['GET'])(self.api_quiz_recommendations)
        
        # Static file routes
        self.app.route('/static/<path:filename>')(self.serve_static)
        
        # Error handlers
        self.app.errorhandler(404)(self.handle_404)
        self.app.errorhandler(500)(self.handle_500)
    
    def index(self) -> str:
        # Execute index operation
    """Main landing page."""
    return render_template('index.html', title='Quiz Dashboard')
    
    def dashboard(self) -> str:
        # Execute dashboard operation
    """Main dashboard with role selection."""
    return render_template('dashboard.html', title='Dashboard')
    
    def student_dashboard(self) -> str:
        # Execute student_dashboard operation
    """Student dashboard with available quizzes and progress."""
    try:
            # Get current user (demo user for now)
            user_id = session.get('user_id', 1)
            
            # Get user statistics
            user_stats = self.sr_engine.get_user_statistics(user_id)
            
            # Get recommended questions
            recommended_questions = self.sr_engine.select_next_questions(user_id, count=10)
            
            # Get question details for recommendations
            question_details = []
            for question_id in recommended_questions:
                question = self.question_manager.get_question(question_id)
                if question:
                    question_details.append(question)
            
            return render_template('student_dashboard.html',
                                 title='Student Dashboard',
                                 user_stats=user_stats,
                                 recommended_questions=question_details)
                                 
        except Exception as e:
            logger.error(f"Student dashboard error: {e}")
            flash(f"Error loading dashboard: {str(e)}", 'error')
            return render_template('error.html', error=str(e))
    
    def instructor_dashboard(self) -> str:
        # Execute instructor_dashboard operation
    """Instructor dashboard with question management and analytics."""
    try:
            # Get recent questions
            recent_questions = self.question_manager.search_questions(limit=10)
            
            # Get question type distribution
            type_stats = self._get_question_type_statistics()
            
            return render_template('instructor_dashboard.html',
                                 title='Instructor Dashboard',
                                 recent_questions=recent_questions,
                                 type_stats=type_stats)
                                 
        except Exception as e:
            logger.error(f"Instructor dashboard error: {e}")
            flash(f"Error loading dashboard: {str(e)}", 'error')
            return render_template('error.html', error=str(e))
    
    def start_quiz_session(self) -> str:
        # Execute start_quiz_session operation
    """Start new quiz session."""
    try:
            # Get session parameters
            user_id = session.get('user_id', 1)
            question_count = int(request.form.get('question_count', 10))
            difficulty_level = request.form.get('difficulty_level')
            hashtags = request.form.getlist('hashtags')
            
            # Create new quiz session
            session_uuid = str(uuid.uuid4())
            session_config = {
                'question_count': question_count,
                'difficulty_level': int(difficulty_level) if difficulty_level else None,
                'hashtags': hashtags,
                'adaptive_difficulty': request.form.get('adaptive_difficulty') == 'on',
                'spaced_repetition': request.form.get('spaced_repetition') == 'on'
            }
            
            # Insert session into database
            query = """
                INSERT INTO quiz_sessions (
                    user_id, session_uuid, status, total_questions, session_config_json
                ) VALUES (?, ?, ?, ?, ?)
            """
            
            params = (
                user_id,
                session_uuid,
                QuizSessionStatus.ACTIVE.value,
                question_count,
                json.dumps(session_config)
            )
            
            self.database.execute_update(query, params)
            
            logger.info(f"Quiz session started: {session_uuid} for user {user_id}")
            return redirect(url_for('quiz_interface', session_id=session_uuid))
            
        except Exception as e:
            logger.error(f"Failed to start quiz session: {e}")
            flash(f"Error starting quiz: {str(e)}", 'error')
            return redirect(url_for('student_dashboard'))
    
    def quiz_interface(self, session_id: str) -> str:
        # Execute quiz_interface operation
    """Main quiz taking interface."""
    try:
            # Validate session
            session_data = self._get_quiz_session(session_id)
            if not session_data:
                flash("Quiz session not found or expired", 'error')
                return redirect(url_for('student_dashboard'))
            
            # Check if session is still active
            if session_data['status'] != QuizSessionStatus.ACTIVE.value:
                flash("Quiz session is no longer active", 'error')
                return redirect(url_for('student_dashboard'))
            
            return render_template('quiz_interface.html',
                                 title='Quiz Session',
                                 session_id=session_id,
                                 session_data=session_data)
                                 
        except Exception as e:
            logger.error(f"Quiz interface error: {e}")
            flash(f"Error loading quiz: {str(e)}", 'error')
            return redirect(url_for('student_dashboard'))
    
    def get_next_question(self, session_id: str) -> Dict[str, Any]:
        # Execute get_next_question operation
    """API endpoint to get next question in quiz session."""
    try:
            # Validate session
            session_data = self._get_quiz_session(session_id)
            if not session_data:
                return jsonify({'error': 'Session not found'}), 404
            
            # Check if quiz is complete
            if session_data['questions_answered'] >= session_data['total_questions']:
                return jsonify({'complete': True, 'message': 'Quiz completed'})
            
            # Get session configuration
            session_config = json.loads(session_data['session_config_json'])
            user_id = session_data['user_id']
            
            # Select next question based on configuration
            if session_config.get('spaced_repetition', False):
                # Use spaced repetition algorithm
                question_ids = self.sr_engine.select_next_questions(
                    user_id=user_id,
                    count=1,
                    preferred_hashtags=session_config.get('hashtags'),
                    target_difficulty=session_config.get('difficulty_level')
                )
            else:
                # Use simple random selection with filters
                question_ids = self._select_random_questions(
                    count=1,
                    difficulty_level=session_config.get('difficulty_level'),
                    hashtags=session_config.get('hashtags')
                )
            
            if not question_ids:
                return jsonify({'error': 'No more questions available'}), 404
            
            # Get question details
            question = self.question_manager.get_question(question_ids[0])
            if not question:
                return jsonify({'error': 'Question not found'}), 404
            
            # Track question in session
            self._track_question_in_session(session_id, question_ids[0])
            
            # Prepare question for client (remove correct answers)
            client_question = self._prepare_question_for_client(question)
            
            return jsonify({
                'question': client_question,
                'session_progress': {
                    'current': session_data['questions_answered'] + 1,
                    'total': session_data['total_questions']
                }
            })
            
        except Exception as e:
            logger.error(f"Get next question error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def submit_question_answer(self, session_id: str) -> Dict[str, Any]:
        # Execute submit_question_answer operation
    """API endpoint to submit question answer."""
    try:
            # Validate session
            session_data = self._get_quiz_session(session_id)
            if not session_data:
                return jsonify({'error': 'Session not found'}), 404
            
            # Get answer data
            answer_data = request.get_json()
            question_id = answer_data.get('question_id')
            user_answer = answer_data.get('answer')
            time_taken = answer_data.get('time_taken_seconds', 0)
            confidence_level = answer_data.get('confidence_level', 3)
            
            if not question_id or user_answer is None:
                return jsonify({'error': 'Missing question ID or answer'}), 400
            
            # Get question details
            question = self.question_manager.get_question(question_id)
            if not question:
                return jsonify({'error': 'Question not found'}), 404
            
            # Evaluate answer
            evaluation_result = self._evaluate_answer(question, user_answer)
            
            # Calculate performance score (0-5 scale for SM-2)
            performance_score = self._calculate_performance_score(
                evaluation_result['is_correct'],
                time_taken,
                confidence_level,
                question['estimated_time']
            )
            
            # Record attempt in database
            attempt_id = self._record_quiz_attempt(
                session_id=session_id,
                question_id=question_id,
                user_id=session_data['user_id'],
                user_answer=user_answer,
                is_correct=evaluation_result['is_correct'],
                time_taken=time_taken,
                confidence_level=confidence_level,
                performance_score=performance_score
            )
            
            # Update spaced repetition progress
            progress = self.sr_engine.process_question_attempt(
                user_id=session_data['user_id'],
                question_id=question_id,
                performance_score=performance_score,
                time_taken_seconds=time_taken,
                is_correct=evaluation_result['is_correct']
            )
            
            # Update session progress
            self._update_session_progress(session_id, evaluation_result['is_correct'])
            
            # Prepare response
            response = {
                'correct': evaluation_result['is_correct'],
                'score': evaluation_result.get('score', 0),
                'explanation': question.get('explanation', ''),
                'correct_answer': evaluation_result.get('correct_answer'),
                'performance_score': performance_score,
                'next_review_date': progress.next_review_date.isoformat() if progress.next_review_date else None,
                'mastery_level': round(progress.mastery_level, 1)
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Submit answer error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def complete_quiz_session(self, session_id: str) -> Dict[str, Any]:
        # Execute complete_quiz_session operation
    """API endpoint to complete quiz session."""
    try:
            # Get session data
            session_data = self._get_quiz_session(session_id)
            if not session_data:
                return jsonify({'error': 'Session not found'}), 404
            
            # Update session status
            query = """
                UPDATE quiz_sessions 
                SET status = ?, completed_at = ?
                WHERE session_uuid = ?
            """
            
            self.database.execute_update(query, (
                QuizSessionStatus.COMPLETED.value,
                datetime.now().isoformat(),
                session_id
            ))
            
            # Calculate final statistics
            final_stats = self._calculate_session_statistics(session_id)
            
            logger.info(f"Quiz session completed: {session_id}")
            
            return jsonify({
                'message': 'Quiz completed successfully',
                'statistics': final_stats
            })
            
        except Exception as e:
            logger.error(f"Complete session error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def create_question(self) -> str:
        # Execute create_question operation
    """Create new question interface."""
    if request.method == 'GET':
            return render_template('create_question.html',
                                 title='Create Question',
                                 question_types=[t.value for t in QuestionType])
        
        try:
            # Get form data
            question_data = self._extract_question_from_form(request.form)
            
            # Validate question
            validation_result = self.question_manager.validator.validate_question(question_data)
            
            if not validation_result.is_valid:
                flash(f"Validation errors: {', '.join(validation_result.errors)}", 'error')
                return render_template('create_question.html',
                                     title='Create Question',
                                     question_types=[t.value for t in QuestionType],
                                     form_data=request.form)
            
            # Create question
            question_id = self.question_manager.create_question(question_data, created_by=1)
            
            if question_id:
                flash(f"Question created successfully! ID: {question_id}", 'success')
                return redirect(url_for('view_question', question_id=question_id))
            else:
                flash("Failed to create question", 'error')
                
        except Exception as e:
            logger.error(f"Create question error: {e}")
            flash(f"Error creating question: {str(e)}", 'error')
        
        return render_template('create_question.html',
                             title='Create Question',
                             question_types=[t.value for t in QuestionType],
                             form_data=request.form)
    
    def list_questions(self) -> str:
        # Execute list_questions operation
    """List all questions with filtering."""
    try:
            # Get filter parameters
            question_type = request.args.get('type')
            difficulty = request.args.get('difficulty')
            search_text = request.args.get('search')
            hashtags = request.args.getlist('hashtags')
            
            # Build difficulty range
            difficulty_range = None
            if difficulty:
                try:
                    diff_int = int(difficulty)
                    difficulty_range = (diff_int, diff_int)
                except ValueError:
                    pass
            
            # Search questions
            questions = self.question_manager.search_questions(
                question_type=question_type,
                hashtags=hashtags if hashtags else None,
                difficulty_range=difficulty_range,
                search_text=search_text,
                limit=100
            )
            
            return render_template('list_questions.html',
                                 title='Questions',
                                 questions=questions,
                                 filters={
                                     'type': question_type,
                                     'difficulty': difficulty,
                                     'search': search_text,
                                     'hashtags': hashtags
                                 },
                                 question_types=[t.value for t in QuestionType])
                                 
        except Exception as e:
            logger.error(f"List questions error: {e}")
            flash(f"Error loading questions: {str(e)}", 'error')
            return render_template('error.html', error=str(e))
    
    def view_question(self, question_id: int) -> str:
        # Execute view_question operation
    """View individual question details."""
    try:
            question = self.question_manager.get_question(question_id)
            
            if not question:
                flash("Question not found", 'error')
                return redirect(url_for('list_questions'))
            
            return render_template('view_question.html',
                                 title=f'Question: {question["title"]}',
                                 question=question)
                                 
        except Exception as e:
            logger.error(f"View question error: {e}")
            flash(f"Error loading question: {str(e)}", 'error')
            return redirect(url_for('list_questions'))
    
    def import_questions(self) -> str:
        # Execute import_questions operation
    """Import questions from JSON file."""
    if request.method == 'GET':
            return render_template('import_questions.html', title='Import Questions')
        
        try:
            # Check if file was uploaded
            if 'questions_file' not in request.files:
                flash("No file selected", 'error')
                return render_template('import_questions.html', title='Import Questions')
            
            file = request.files['questions_file']
            
            if file.filename == '':
                flash("No file selected", 'error')
                return render_template('import_questions.html', title='Import Questions')
            
            # Validate file extension
            if not file.filename.endswith('.json'):
                flash("Only JSON files are supported", 'error')
                return render_template('import_questions.html', title='Import Questions')
            
            # Save uploaded file temporarily
            temp_path = f"/tmp/questions_import_{uuid.uuid4().hex}.json"
            file.save(temp_path)
            
            try:
                # Import questions
                import_result = self.question_manager.import_questions(temp_path)
                
                # Display results
                flash(f"Import completed: {import_result['imported']}/{import_result['total']} questions imported", 
                      'success' if import_result['imported'] > 0 else 'warning')
                
                if import_result['errors']:
                    flash(f"Errors: {'; '.join(import_result['errors'][:5])}", 'error')
                
                if import_result['warnings']:
                    flash(f"Warnings: {'; '.join(import_result['warnings'][:5])}", 'warning')
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            if import_result['imported'] > 0:
                return redirect(url_for('list_questions'))
                
        except Exception as e:
            logger.error(f"Import questions error: {e}")
            flash(f"Error importing questions: {str(e)}", 'error')
        
        return render_template('import_questions.html', title='Import Questions')
    
    def analytics_dashboard(self) -> str:
        # Execute analytics_dashboard operation
    """Analytics dashboard with system statistics."""
    try:
            # Get system-wide statistics
            system_stats = self._get_system_statistics()
            
            return render_template('analytics_dashboard.html',
                                 title='Analytics Dashboard',
                                 system_stats=system_stats)
                                 
        except Exception as e:
            logger.error(f"Analytics dashboard error: {e}")
            flash(f"Error loading analytics: {str(e)}", 'error')
            return render_template('error.html', error=str(e))
    
    def user_analytics(self, user_id: int) -> str:
        # Execute user_analytics operation
    """Individual user analytics page."""
    try:
            # Get user statistics
            user_stats = self.sr_engine.get_user_statistics(user_id)
            
            return render_template('user_analytics.html',
                                 title=f'User Analytics - User {user_id}',
                                 user_stats=user_stats,
                                 user_id=user_id)
                                 
        except Exception as e:
            logger.error(f"User analytics error: {e}")
            flash(f"Error loading user analytics: {str(e)}", 'error')
            return render_template('error.html', error=str(e))
    
    # API endpoints
    
    def api_search_questions(self) -> Dict[str, Any]:
        # Execute api_search_questions operation
    """API endpoint for question search."""
    try:
            # Get search parameters
            question_type = request.args.get('type')
            hashtags = request.args.getlist('hashtags')
            difficulty = request.args.get('difficulty')
            search_text = request.args.get('q')
            limit = min(int(request.args.get('limit', 20)), 100)
            
            difficulty_range = None
            if difficulty:
                try:
                    diff_int = int(difficulty)
                    difficulty_range = (diff_int, diff_int)
                except ValueError:
                    pass
            
            # Search questions
            questions = self.question_manager.search_questions(
                question_type=question_type,
                hashtags=hashtags if hashtags else None,
                difficulty_range=difficulty_range,
                search_text=search_text,
                limit=limit
            )
            
            return jsonify({
                'questions': questions,
                'total': len(questions)
            })
            
        except Exception as e:
            logger.error(f"API search error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def api_validate_question(self) -> Dict[str, Any]:
        # Execute api_validate_question operation
    """API endpoint for question validation."""
    try:
            question_data = request.get_json()
            
            if not question_data:
                return jsonify({'error': 'No question data provided'}), 400
            
            # Validate question
            validation_result = self.question_manager.validator.validate_question(question_data)
            
            return jsonify({
                'is_valid': validation_result.is_valid,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings,
                'suggestions': validation_result.suggestions,
                'estimated_difficulty': validation_result.estimated_difficulty,
                'detected_topics': validation_result.detected_topics,
                'latex_content': validation_result.latex_content
            })
            
        except Exception as e:
            logger.error(f"API validation error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def api_user_progress(self, user_id: int) -> Dict[str, Any]:
        # Execute api_user_progress operation
    """API endpoint for user progress data."""
    try:
            user_stats = self.sr_engine.get_user_statistics(user_id)
            return jsonify(user_stats)
            
        except Exception as e:
            logger.error(f"API user progress error: {e}")
            return jsonify({'error': str(e)}), 500
    
    def api_quiz_recommendations(self, user_id: int) -> Dict[str, Any]:
        # Execute api_quiz_recommendations operation
    """API endpoint for quiz question recommendations."""
    try:
            count = min(int(request.args.get('count', 10)), 50)
            hashtags = request.args.getlist('hashtags')
            difficulty = request.args.get('difficulty')
            
            target_difficulty = int(difficulty) if difficulty else None
            
            # Get recommendations
            question_ids = self.sr_engine.select_next_questions(
                user_id=user_id,
                count=count,
                preferred_hashtags=hashtags if hashtags else None,
                target_difficulty=target_difficulty
            )
            
            # Get question details
            questions = []
            for question_id in question_ids:
                question = self.question_manager.get_question(question_id)
                if question:
                    questions.append(question)
            
            return jsonify({
                'recommendations': questions,
                'count': len(questions),
                'user_id': user_id
            })
            
        except Exception as e:
            logger.error(f"API recommendations error: {e}")
            return jsonify({'error': str(e)}), 500
    
    # Helper methods
    
    def _get_quiz_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        # Execute _get_quiz_session operation
    """Get quiz session data by UUID."""
    try:
            query = """
                SELECT user_id, session_uuid, started_at, completed_at, status,
                       total_questions, questions_answered, correct_answers,
                       total_time_seconds, session_config_json
                FROM quiz_sessions
                WHERE session_uuid = ?
            """
            
            results = self.database.execute_query(query, (session_id,))
            
            if not results:
                return None
            
            row = results[0]
            
            return {
                'user_id': row['user_id'],
                'session_uuid': row['session_uuid'],
                'started_at': row['started_at'],
                'completed_at': row['completed_at'],
                'status': row['status'],
                'total_questions': row['total_questions'],
                'questions_answered': row['questions_answered'],
                'correct_answers': row['correct_answers'],
                'total_time_seconds': row['total_time_seconds'],
                'session_config_json': row['session_config_json']
            }
            
        except Exception as e:
            logger.error(f"Failed to get quiz session: {e}")
            return None
    
    def _prepare_question_for_client(self, question: Dict[str, Any]) -> Dict[str, Any]:
        # Execute _prepare_question_for_client operation
    """Prepare question data for client (remove answers)."""
    # Create copy without correct answers
        client_question = question.copy()
        
        # Remove correct answer fields based on question type
        question_type = question['type']
        
        if question_type == QuestionType.MULTIPLE_CHOICE.value:
            # Keep options but remove correct answer indication
            pass
        elif question_type == QuestionType.TRUE_FALSE.value:
            # Remove correct answer
            client_question.pop('correct_answer', None)
        elif question_type == QuestionType.FILL_IN_BLANK.value:
            # Remove acceptable answers
            client_question.pop('acceptable_answers', None)
        elif question_type == QuestionType.REORDER_SEQUENCE.value:
            # Remove correct order
            client_question.pop('correct_order', None)
        elif question_type == QuestionType.MATCHING_PAIRS.value:
            # Remove correct matches
            client_question.pop('correct_matches', None)
        
        return client_question
    
    def _evaluate_answer(self, question: Dict[str, Any], user_answer: Any) -> Dict[str, Any]:
        # Execute _evaluate_answer operation
    """Evaluate user answer against correct answer."""
    question_type = question['type']
        result = {'is_correct': False, 'score': 0}
        
        try:
            if question_type == QuestionType.MULTIPLE_CHOICE.value:
                result = self._evaluate_multiple_choice(question, user_answer)
            elif question_type == QuestionType.TRUE_FALSE.value:
                result = self._evaluate_true_false(question, user_answer)
            elif question_type == QuestionType.FILL_IN_BLANK.value:
                result = self._evaluate_fill_in_blank(question, user_answer)
            elif question_type == QuestionType.REORDER_SEQUENCE.value:
                result = self._evaluate_reorder(question, user_answer)
            elif question_type == QuestionType.MATCHING_PAIRS.value:
                result = self._evaluate_matching(question, user_answer)
            
        except Exception as e:
            logger.error(f"Answer evaluation error: {e}")
            result = {'is_correct': False, 'score': 0, 'error': str(e)}
        
        return result
    
    def _evaluate_multiple_choice(self, question: Dict[str, Any], user_answer: Any) -> Dict[str, Any]:
        # Execute _evaluate_multiple_choice operation
    """Evaluate multiple choice answer."""
    correct_answer = question['correct_answer']
        is_correct = str(user_answer) == str(correct_answer)
        
        return {
            'is_correct': is_correct,
            'score': 100 if is_correct else 0,
            'correct_answer': correct_answer
        }
    
    def _evaluate_true_false(self, question: Dict[str, Any], user_answer: Any) -> Dict[str, Any]:
        # Execute _evaluate_true_false operation
    """Evaluate true/false answer."""
    correct_answer = question['correct_answer']
        user_bool = str(user_answer).lower() in ('true', '1', 'yes')
        is_correct = user_bool == correct_answer
        
        return {
            'is_correct': is_correct,
            'score': 100 if is_correct else 0,
            'correct_answer': correct_answer
        }
    
    def _evaluate_fill_in_blank(self, question: Dict[str, Any], user_answer: Any) -> Dict[str, Any]:
        # Execute _evaluate_fill_in_blank operation
    """Evaluate fill-in-blank answer."""
    acceptable_answers = question['acceptable_answers']
        case_sensitive = question.get('case_sensitive', False)
        
        user_text = str(user_answer).strip()
        if not case_sensitive:
            user_text = user_text.lower()
            acceptable_answers = [ans.lower() for ans in acceptable_answers]
        
        is_correct = user_text in acceptable_answers
        
        return {
            'is_correct': is_correct,
            'score': 100 if is_correct else 0,
            'correct_answer': acceptable_answers[0] if acceptable_answers else ''
        }
    
    def _evaluate_reorder(self, question: Dict[str, Any], user_answer: Any) -> Dict[str, Any]:
        # Execute _evaluate_reorder operation
    """Evaluate reorder/sequence answer."""
    correct_order = question['correct_order']
        user_order = user_answer if isinstance(user_answer, list) else []
        
        # Calculate partial credit
        if question.get('partial_credit', True):
            # Score based on correct positions
            score = 0
            for i, correct_id in enumerate(correct_order):
                if i < len(user_order) and user_order[i] == correct_id:
                    score += 1
            
            score = (score / len(correct_order)) * 100 if correct_order else 0
        else:
            # All or nothing scoring
            score = 100 if user_order == correct_order else 0
        
        return {
            'is_correct': user_order == correct_order,
            'score': score,
            'correct_answer': correct_order
        }
    
    def _evaluate_matching(self, question: Dict[str, Any], user_answer: Any) -> Dict[str, Any]:
        # Execute _evaluate_matching operation
    """Evaluate matching pairs answer."""
    correct_matches = question['correct_matches']
        user_matches = user_answer if isinstance(user_answer, list) else []
        
        # Convert to sets for comparison
        correct_pairs = {(match['left_id'], match['right_id']) for match in correct_matches}
        user_pairs = set()
        
        for match in user_matches:
            if isinstance(match, dict) and 'left_id' in match and 'right_id' in match:
                user_pairs.add((match['left_id'], match['right_id']))
        
        # Calculate score based on correct matches
        correct_count = len(correct_pairs & user_pairs)
        total_count = len(correct_pairs)
        
        score = (correct_count / total_count) * 100 if total_count > 0 else 0
        is_correct = score == 100
        
        return {
            'is_correct': is_correct,
            'score': score,
            'correct_answer': correct_matches
        }
    
    def _calculate_performance_score(self, 
        # _calculate_performance_score operation implementation
                                   is_correct: bool,
    """Execute _calculate_performance_score operation."""
                                   time_taken: float,
                                   confidence_level: int,
                                   estimated_time: int) -> float:
    """Calculate performance score (0-5) for SM-2 algorithm."""
    # Base score from correctness
        if is_correct:
            base_score = 4.0  # Good performance
        else:
            base_score = 1.0  # Poor performance
        
        # Adjust based on time efficiency
        if is_correct and time_taken > 0 and estimated_time > 0:
            time_ratio = time_taken / estimated_time
            
            if time_ratio < 0.5:
                # Very fast - increase score
                base_score = min(5.0, base_score + 0.5)
            elif time_ratio > 2.0:
                # Very slow - decrease score
                base_score = max(0.5, base_score - 0.5)
        
        # Adjust based on confidence level (1-5)
        confidence_adjustment = (confidence_level - 3) * 0.2
        base_score += confidence_adjustment
        
        # Clamp to valid range
        return max(0.0, min(5.0, base_score))
    
    def _record_quiz_attempt(self, **kwargs) -> int:
        # Execute _record_quiz_attempt operation
    """Record quiz attempt in database."""
    query = """
            INSERT INTO quiz_attempts (
                session_id, question_id, user_id, attempted_at, user_answer_json,
                is_correct, time_taken_seconds, confidence_level
            ) VALUES (
                (SELECT id FROM quiz_sessions WHERE session_uuid = ?),
                ?, ?, ?, ?, ?, ?, ?
            )
        """
        
        params = (
            kwargs['session_id'],
            kwargs['question_id'],
            kwargs['user_id'],
            datetime.now().isoformat(),
            json.dumps(kwargs['user_answer']),
            kwargs['is_correct'],
            kwargs['time_taken'],
            kwargs['confidence_level']
        )
        
        self.database.execute_update(query, params)
        
        # Get the inserted attempt ID
        result = self.database.execute_query("SELECT last_insert_rowid()")
        return result[0][0] if result else 0
    
    def _update_session_progress(self, session_id: str, is_correct: bool) -> None:
        # Execute _update_session_progress operation
    """Update quiz session progress."""
    query = """
            UPDATE quiz_sessions 
            SET questions_answered = questions_answered + 1,
                correct_answers = correct_answers + ?,
                total_time_seconds = total_time_seconds + ?
            WHERE session_uuid = ?
        """
        
        params = (
            1 if is_correct else 0,
            0,  # Time will be updated separately if needed
            session_id
        )
        
        self.database.execute_update(query, params)
    
    def _track_question_in_session(self, session_id: str, question_id: int) -> None:
        # Execute _track_question_in_session operation
    """Track that a question was shown in session."""
    # This could be implemented to prevent showing the same question twice
        pass
    
    def _select_random_questions(self, 
        # _select_random_questions operation implementation
                                count: int = 1,
    """Execute _select_random_questions operation."""
                                difficulty_level: Optional[int] = None,
                                hashtags: Optional[List[str]] = None) -> List[int]:
    """Simple random question selection with filters."""
    try:
            conditions = ["is_active = 1"]
            params = []
            
            if difficulty_level is not None:
                conditions.append("difficulty_level = ?")
                params.append(difficulty_level)
            
            if hashtags:
                hashtag_conditions = []
                for tag in hashtags:
                    hashtag_conditions.append("hashtags LIKE ?")
                    params.append(f"%\"{tag}\"%")
                conditions.append(f"({' OR '.join(hashtag_conditions)})")
            
            query = f"""
                SELECT id FROM questions
                WHERE {' AND '.join(conditions)}
                ORDER BY RANDOM()
                LIMIT ?
            """
            params.append(count)
            
            results = self.database.execute_query(query, tuple(params))
            return [row['id'] for row in results]
            
        except Exception as e:
            logger.error(f"Random question selection error: {e}")
            return []
    
def _extract_question_from_form(self, form_data: Any) -> Dict[str, Any]:
    # Execute _extract_question_from_form operation
    """Extract question data from form submission."""
    question_type = form_data.get('question_type')
        
        # Base question data
        question_data = {
            'type': question_type,
            'title': form_data.get('title', ''),
            'content': form_data.get('content', ''),
            'explanation': form_data.get('explanation', ''),
            'difficulty': int(form_data.get('difficulty', 3)),
            'estimated_time': int(form_data.get('estimated_time', 60)),
            'hashtags': [tag.strip() for tag in form_data.get('hashtags', '').split(',') if tag.strip()]
        }
        
        # Add type-specific data
        if question_type == QuestionType.MULTIPLE_CHOICE.value:
            options = []
            option_texts = form_data.getlist('option_text')
            option_ids = form_data.getlist('option_id')
            
            for i, text in enumerate(option_texts):
                if text.strip():
                    options.append({
                        'id': option_ids[i] if i < len(option_ids) else f'option_{i}',
                        'text': text.strip()
                    })
            
            question_data.update({
                'options': options,
                'correct_answer': form_data.get('correct_answer', ''),
                'shuffle_options': form_data.get('shuffle_options') == 'on'
            })
        
        elif question_type == QuestionType.TRUE_FALSE.value:
            question_data.update({
                'correct_answer': form_data.get('correct_answer') == 'true'
            })
        
        elif question_type == QuestionType.FILL_IN_BLANK.value:
            acceptable_answers = [
                ans.strip() for ans in form_data.get('acceptable_answers', '').split('\n')
                if ans.strip()
            ]
            
            question_data.update({
                'acceptable_answers': acceptable_answers,
                'case_sensitive': form_data.get('case_sensitive') == 'on'
            })
        
        return question_data
    
    def _get_question_type_statistics(self) -> Dict[str, int]:
        # Execute _get_question_type_statistics operation
    """Get question count by type."""
    try:
            query = """
                SELECT question_type, COUNT(*) as count
                FROM questions
                WHERE is_active = 1
                GROUP BY question_type
            """
            
            results = self.database.execute_query(query)
            
            return {row['question_type']: row['count'] for row in results}
            
        except Exception as e:
            logger.error(f"Question type statistics error: {e}")
            return {}
    
    def _get_system_statistics(self) -> Dict[str, Any]:
        # Execute _get_system_statistics operation
    """Get system-wide statistics."""
    try:
            stats = {}
            
            # Question statistics
            question_stats = self.database.execute_query("""
                SELECT 
                    COUNT(*) as total_questions,
                    COUNT(CASE WHEN is_active = 1 THEN 1 END) as active_questions,
                    AVG(difficulty_level) as avg_difficulty
                FROM questions
            """)
            
            if question_stats:
                stats.update({
                    'total_questions': question_stats[0]['total_questions'],
                    'active_questions': question_stats[0]['active_questions'],
                    'avg_difficulty': round(question_stats[0]['avg_difficulty'] or 0, 2)
                })
            
            # User statistics
            user_stats = self.database.execute_query("""
                SELECT 
                    COUNT(DISTINCT user_id) as active_users,
                    AVG(mastery_level) as avg_mastery,
                    SUM(total_attempts) as total_attempts
                FROM user_progress
                WHERE total_attempts > 0
            """)
            
            if user_stats:
                stats.update({
                    'active_users': user_stats[0]['active_users'],
                    'avg_mastery': round(user_stats[0]['avg_mastery'] or 0, 2),
                    'total_attempts': user_stats[0]['total_attempts'] or 0
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"System statistics error: {e}")
            return {}
    
    def _calculate_session_statistics(self, session_id: str) -> Dict[str, Any]:
        # Execute _calculate_session_statistics operation
    """Calculate final statistics for completed session."""
    try:
            # Session data
            session_data = self._get_quiz_session(session_id)
            if not session_data:
                return {}
            
            # Detailed attempt statistics
            attempt_stats = self.database.execute_query("""
                SELECT 
                    COUNT(*) as total_attempts,
                    COUNT(CASE WHEN is_correct = 1 THEN 1 END) as correct_attempts,
                    AVG(time_taken_seconds) as avg_time,
                    MIN(time_taken_seconds) as min_time,
                    MAX(time_taken_seconds) as max_time
                FROM quiz_attempts qa
                JOIN quiz_sessions qs ON qa.session_id = qs.id
                WHERE qs.session_uuid = ?
            """, (session_id,))
            
            stats = {
                'session_id': session_id,
                'total_questions': session_data['total_questions'],
                'questions_answered': session_data['questions_answered'],
                'correct_answers': session_data['correct_answers'],
                'accuracy_percentage': round(
                    (session_data['correct_answers'] / max(session_data['questions_answered'], 1)) * 100, 2
                ),
                'completion_percentage': round(
                    (session_data['questions_answered'] / max(session_data['total_questions'], 1)) * 100, 2
                )
            }
            
            if attempt_stats:
                row = attempt_stats[0]
                stats.update({
                    'average_time_per_question': round(row['avg_time'] or 0, 2),
                    'fastest_answer': round(row['min_time'] or 0, 2),
                    'slowest_answer': round(row['max_time'] or 0, 2)
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"Session statistics error: {e}")
            return {'error': str(e)}
    
    # Static file and error handlers
    
def serve_static(self, filename -> Any: str):
    # Execute serve_static operation
        """Serve static files."""
        return send_from_directory(self.app.static_folder, filename)
    
def handle_404(self, error -> Any: Any):
        """Handle 404 errors."""
        return render_template('error.html', 
                             error="Page not found",
                             error_code=404), 404
    
def handle_500(self, error -> Any: Any):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return render_template('error.html',
                             error="Internal server error",
                             error_code=500), 500
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False) -> None:
    """Run Flask development server."""
    logger.info(f"Starting Quiz Dashboard web server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


def create_app(database_path: str = "quiz_dashboard.db") -> QuizWebApp:
    """Create and configure Quiz Dashboard web application."""
    return QuizWebApp(database_path=database_path)