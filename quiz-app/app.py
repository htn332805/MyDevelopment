# quiz-app/app.py

"""
Main Dash application for the Interactive Quiz System.

This module provides a comprehensive quiz application including:
- Multi-type question support (MCQ, T/F, Fill-in, Reorder, Matching)
- Real-time MathJax rendering for LaTeX content
- Adaptive quiz generation with spaced repetition
- Performance analytics and progress tracking
- Responsive UI with Bootstrap components
- Session management and user authentication

Integrates with Framework0's component system for consistency and robustness.
"""

import os
import sys
import time
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
import threading
import random

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dash and Plotly imports
import dash
from dash import dcc, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

# Framework0 imports
from src.core.logger import get_logger
from src.core.interfaces import ComponentLifecycle, Configurable
from src.core.decorators_v2 import monitor_resources, debug_trace

# Import quiz components
sys.path.append(".")  # Add current directory
from models.storage import get_quiz_database, QuizDatabase
from utils.qloader import get_question_loader, QuestionLoader
from utils.selection import get_spaced_repetition_selector, select_quiz_questions, SelectionCriteria

# Initialize logger with debug support
logger = get_logger(__name__, debug=True)


class QuizSession:
    """Manages individual quiz session state."""
    
    def __init__(self, user_id: int, questions: List[Dict[str, Any]]):
        """Initialize quiz session."""
        self.session_id = str(uuid.uuid4())  # Unique session identifier
        self.user_id = user_id  # User taking the quiz
        self.questions = questions  # List of questions in this session
        self.current_index = 0  # Current question index
        self.start_time = time.time()  # Session start time
        self.question_start_time = time.time()  # Current question start time
        self.answers = {}  # User answers by question_id
        self.scores = {}  # Question scores by question_id
        self.hints_used = set()  # Questions where hint was used
        self.completed = False  # Whether quiz is completed
        
    def get_current_question(self) -> Optional[Dict[str, Any]]:
        """Get current question or None if quiz complete."""
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None
    
    def get_question_timing(self) -> float:
        """Get time spent on current question in seconds."""
        return time.time() - self.question_start_time
    
    def submit_answer(self, answer: Any, used_hint: bool = False) -> bool:
        """Submit answer for current question."""
        current_question = self.get_current_question()
        if not current_question:
            return False
        
        question_id = str(current_question['question_id'])
        correct = self._evaluate_answer(current_question, answer)
        latency = self.get_question_timing()
        
        # Store answer and score
        self.answers[question_id] = answer
        self.scores[question_id] = {
            'correct': correct,
            'latency': latency,
            'hint_used': used_hint,
            'timestamp': datetime.now()
        }
        
        if used_hint:
            self.hints_used.add(question_id)
        
        # Move to next question
        self.current_index += 1
        self.question_start_time = time.time()
        
        # Mark completed if last question
        if self.current_index >= len(self.questions):
            self.completed = True
        
        return correct
    
    def _evaluate_answer(self, question: Dict[str, Any], answer: Any) -> bool:
        """Evaluate if answer is correct."""
        question_type = question['type']
        correct_answer = question['answer']
        
        try:
            if question_type == 'multiple_choice':
                return int(answer) == correct_answer
            
            elif question_type == 'true_false':
                return bool(answer) == correct_answer
            
            elif question_type == 'fill_blank':
                if isinstance(correct_answer, list):
                    # Check if answer matches any acceptable answer
                    answer_str = str(answer).strip().lower()
                    return any(answer_str == str(acc).strip().lower() for acc in correct_answer)
                else:
                    return str(answer).strip().lower() == str(correct_answer).strip().lower()
            
            elif question_type == 'reorder':
                correct_order = question['reorder']
                return answer == correct_order
            
            elif question_type == 'matching':
                # Answer should be a dict of {left_index: right_index}
                correct_pairs = {pair[0]: pair[1] for pair in question['matching']['pairs']}
                return answer == correct_pairs
            
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating answer: {e}")
            return False
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current quiz progress."""
        total = len(self.questions)
        completed = self.current_index
        correct = sum(1 for score in self.scores.values() if score['correct'])
        
        return {
            'total_questions': total,
            'completed_questions': completed,
            'correct_answers': correct,
            'accuracy': correct / max(completed, 1),
            'progress_percent': (completed / total) * 100,
            'time_elapsed': time.time() - self.start_time,
            'completed': self.completed
        }


class QuizApp(ComponentLifecycle, Configurable):
    """Main Quiz Dash Application."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8050, debug: bool = True):
        """Initialize Quiz Application."""
        super().__init__()
        self.host = host  # Server host
        self.port = port  # Server port  
        self.debug = debug  # Debug mode
        
        # Initialize Dash app with Bootstrap theme
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True,
            assets_folder='assets'
        )
        
        # Component instances
        self.db: Optional[QuizDatabase] = None  # Database connection
        self.loader: Optional[QuestionLoader] = None  # Question loader
        self.selector = None  # Question selector
        
        # Session management
        self.sessions: Dict[str, QuizSession] = {}  # Active quiz sessions
        self.session_lock = threading.Lock()  # Thread safety for sessions
        
        # App configuration
        self.app.title = "Interactive Quiz System - Framework0"
        
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Initialize quiz application components."""
        logger.info("Initializing Quiz Application")
        
        # Initialize core components
        self.db = get_quiz_database()
        self.loader = get_question_loader()
        self.selector = get_spaced_repetition_selector()
        
        # Setup app layout and callbacks
        self._setup_layout()
        self._setup_callbacks()
        
        logger.info("Quiz Application initialized successfully")
        
    def _do_cleanup(self) -> None:
        """Cleanup quiz application resources."""
        logger.info("Cleaning up Quiz Application")
        
        # Clear active sessions
        with self.session_lock:
            self.sessions.clear()
        
        logger.info("Quiz Application cleanup completed")
    
    def _setup_layout(self) -> None:
        """Setup the main application layout."""
        logger.debug("Setting up application layout")
        
        self.app.layout = dbc.Container([
            # Store components for state management
            dcc.Store(id='session-store', data=None),
            dcc.Store(id='current-question-store', data=None),
            dcc.Store(id='quiz-config-store', data=None),
            
            # Main header
            dbc.Row([
                dbc.Col([
                    html.H1("Interactive Quiz System", className="text-center mb-4"),
                    html.Hr()
                ])
            ]),
            
            # Quiz content area
            html.Div(id='quiz-content'),
            
            # Footer with Framework0 branding
            dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.P("Powered by Framework0 Quiz System", 
                          className="text-center text-muted small")
                ])
            ], className="mt-5")
            
        ], fluid=True)
    
    def _setup_callbacks(self) -> None:
        """Setup all Dash callbacks."""
        logger.debug("Setting up application callbacks")
        
        # Main page routing callback
        @self.app.callback(
            Output('quiz-content', 'children'),
            [Input('session-store', 'data')]
        )
        def display_quiz_content(session_data):
            """Display appropriate quiz content based on session state."""
            try:
                if not session_data:
                    return self._render_quiz_setup()
                
                session_id = session_data.get('session_id')
                if session_id not in self.sessions:
                    return self._render_quiz_setup()
                
                session = self.sessions[session_id]
                
                if session.completed:
                    return self._render_results(session)
                else:
                    return self._render_question(session)
                    
            except Exception as e:
                logger.error(f"Error displaying quiz content: {e}")
                return self._render_error("Failed to load quiz content")
        
        # Quiz setup callback
        @self.app.callback(
            [Output('session-store', 'data'),
             Output('quiz-config-store', 'data')],
            [Input('start-quiz-btn', 'n_clicks')],
            [State('num-questions', 'value'),
             State('categories-dropdown', 'value'),
             State('hashtags-dropdown', 'value'), 
             State('difficulty-dropdown', 'value')]
        )
        def start_quiz(n_clicks, num_questions, categories, hashtags, difficulty):
            """Start a new quiz with specified parameters."""
            try:
                if not n_clicks:
                    return None, None
                
                # Default values
                num_questions = num_questions or 10
                user_id = 1  # Default user for now
                
                # Get questions using selection algorithm
                questions = select_quiz_questions(
                    user_id=user_id,
                    num_questions=num_questions,
                    categories=categories,
                    hashtags=hashtags,
                    difficulty=difficulty
                )
                
                if not questions:
                    logger.warning("No questions available for selection criteria")
                    return None, None
                
                # Create new quiz session
                session = QuizSession(user_id, questions)
                
                with self.session_lock:
                    self.sessions[session.session_id] = session
                
                logger.info(f"Started new quiz session {session.session_id} with {len(questions)} questions")
                
                session_data = {
                    'session_id': session.session_id,
                    'user_id': user_id
                }
                
                quiz_config = {
                    'num_questions': num_questions,
                    'categories': categories,
                    'hashtags': hashtags,
                    'difficulty': difficulty
                }
                
                return session_data, quiz_config
                
            except Exception as e:
                logger.error(f"Error starting quiz: {e}")
                return None, None
        
        # Answer submission callback
        @self.app.callback(
            [Output('current-question-store', 'data'),
             Output('feedback-modal', 'is_open'),
             Output('feedback-content', 'children')],
            [Input('submit-answer-btn', 'n_clicks'),
             Input('hint-btn', 'n_clicks')],
            [State('session-store', 'data'),
             State('answer-input', 'value'),
             State('current-question-store', 'data')]
        )
        def handle_answer_submission(submit_clicks, hint_clicks, session_data, answer, current_question):
            """Handle answer submission and hint requests."""
            try:
                if not session_data or not submit_clicks:
                    return current_question, False, ""
                
                session_id = session_data['session_id']
                if session_id not in self.sessions:
                    return current_question, False, ""
                
                session = self.sessions[session_id]
                current_q = session.get_current_question()
                
                if not current_q:
                    return current_question, False, ""
                
                # Check if hint was requested
                used_hint = ctx.triggered_id == 'hint-btn' if ctx.triggered else False
                
                if ctx.triggered_id == 'submit-answer-btn':
                    # Submit answer
                    correct = session.submit_answer(answer, used_hint)
                    
                    # Record in database
                    try:
                        self.db.record_attempt(
                            session.user_id,
                            str(current_q['question_id']),
                            correct,
                            str(answer),
                            session.get_question_timing(),
                            used_hint
                        )
                    except Exception as e:
                        logger.error(f"Failed to record attempt: {e}")
                    
                    # Generate feedback
                    feedback = self._generate_feedback(current_q, answer, correct)
                    
                    return {'updated': time.time()}, True, feedback
                
                return current_question, False, ""
                
            except Exception as e:
                logger.error(f"Error handling answer submission: {e}")
                return current_question, False, "Error processing answer"
    
    def _render_quiz_setup(self) -> dbc.Container:
        """Render quiz setup interface."""
        logger.debug("Rendering quiz setup")
        
        # Get available options
        try:
            categories = self.loader.get_all_categories()
            hashtags = self.loader.get_all_hashtags()
        except Exception as e:
            logger.error(f"Error getting quiz options: {e}")
            categories, hashtags = [], []
        
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2("Start New Quiz", className="mb-4"),
                    
                    # Quiz configuration form
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Number of Questions"),
                                dbc.Input(
                                    id='num-questions',
                                    type='number',
                                    value=10,
                                    min=1,
                                    max=50,
                                    step=1
                                )
                            ], md=6),
                            
                            dbc.Col([
                                dbc.Label("Difficulty"),
                                dcc.Dropdown(
                                    id='difficulty-dropdown',
                                    options=[
                                        {'label': 'Easy', 'value': 'easy'},
                                        {'label': 'Medium', 'value': 'medium'},
                                        {'label': 'Hard', 'value': 'hard'}
                                    ],
                                    placeholder="Any difficulty"
                                )
                            ], md=6)
                        ], className="mb-3"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Categories"),
                                dcc.Dropdown(
                                    id='categories-dropdown',
                                    options=[{'label': cat, 'value': cat} for cat in categories],
                                    multi=True,
                                    placeholder="Select categories (optional)"
                                )
                            ], md=6),
                            
                            dbc.Col([
                                dbc.Label("Hashtags"),
                                dcc.Dropdown(
                                    id='hashtags-dropdown',
                                    options=[{'label': tag, 'value': tag} for tag in hashtags],
                                    multi=True,
                                    placeholder="Select hashtags (optional)"
                                )
                            ], md=6)
                        ], className="mb-4"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    "Start Quiz",
                                    id='start-quiz-btn',
                                    color="primary",
                                    size="lg",
                                    className="w-100"
                                )
                            ])
                        ])
                    ])
                ], md=8)
            ], justify="center"),
            
            # Statistics panel
            dbc.Row([
                dbc.Col([
                    self._render_statistics_panel()
                ], md=8)
            ], justify="center", className="mt-5")
            
        ], className="mt-4")
    
    def _render_question(self, session: QuizSession) -> dbc.Container:
        """Render current question interface."""
        current_question = session.get_current_question()
        if not current_question:
            return self._render_error("No question available")
        
        progress = session.get_progress()
        
        return dbc.Container([
            # Progress bar
            dbc.Row([
                dbc.Col([
                    html.H4(f"Question {session.current_index + 1} of {len(session.questions)}"),
                    dbc.Progress(
                        value=progress['progress_percent'],
                        striped=True,
                        className="mb-4"
                    )
                ])
            ]),
            
            # Question content
            dbc.Row([
                dbc.Col([
                    self._render_question_content(current_question, session)
                ], md=10)
            ], justify="center"),
            
            # Action buttons
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button(
                            "Show Hint",
                            id='hint-btn',
                            color="info",
                            outline=True
                        ),
                        dbc.Button(
                            "Submit Answer",
                            id='submit-answer-btn',
                            color="primary"
                        )
                    ], className="w-100")
                ], md=6)
            ], justify="center", className="mt-4"),
            
            # Feedback modal
            dbc.Modal([
                dbc.ModalHeader("Answer Feedback"),
                dbc.ModalBody(id='feedback-content'),
                dbc.ModalFooter([
                    dbc.Button("Continue", id='continue-btn', color="primary")
                ])
            ], id='feedback-modal', is_open=False)
            
        ], className="mt-4")
    
    def _render_question_content(self, question: Dict[str, Any], session: QuizSession) -> html.Div:
        """Render question content based on type."""
        question_type = question['type']
        prompt = question['prompt']
        
        content = [
            html.H4(prompt, className="mb-4"),
            html.Div(id='question-media') if question.get('media') else html.Div()
        ]
        
        # Type-specific input components
        if question_type == 'multiple_choice':
            choices = question['choices']
            content.append(
                dbc.RadioItems(
                    id='answer-input',
                    options=[{'label': choice, 'value': i} for i, choice in enumerate(choices)],
                    className="mb-3"
                )
            )
            
        elif question_type == 'true_false':
            content.append(
                dbc.RadioItems(
                    id='answer-input',
                    options=[
                        {'label': 'True', 'value': True},
                        {'label': 'False', 'value': False}
                    ],
                    className="mb-3"
                )
            )
            
        elif question_type == 'fill_blank':
            content.append(
                dbc.Input(
                    id='answer-input',
                    type='text',
                    placeholder="Enter your answer...",
                    className="mb-3"
                )
            )
            
        elif question_type == 'reorder':
            items = question['reorder']
            shuffled_items = items.copy()
            random.shuffle(shuffled_items)  # Shuffle for user to reorder
            
            content.append(
                html.Div([
                    html.P("Drag items to reorder them correctly:", className="mb-2"),
                    html.Div(id='reorder-container', children=[
                        dbc.ListGroup([
                            dbc.ListGroupItem(item, className="draggable-item") 
                            for item in shuffled_items
                        ])
                    ])
                ])
            )
            
        elif question_type == 'matching':
            matching = question['matching']
            left_items = matching['left']
            right_items = matching['right']
            
            content.append(
                dbc.Row([
                    dbc.Col([
                        html.H5("Match items from left to right:"),
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P(f"{i}: {item}") 
                                    for i, item in enumerate(left_items)
                                ])
                            ], className="mb-3"),
                            dbc.Card([
                                dbc.CardBody([
                                    html.P(f"{i}: {item}") 
                                    for i, item in enumerate(right_items)
                                ])
                            ])
                        ]),
                        html.P("Enter matches as: 0-1,1-0,2-2 (left-right pairs)", className="small text-muted mt-2"),
                        dbc.Input(
                            id='answer-input',
                            type='text',
                            placeholder="Enter matches...",
                            className="mt-2"
                        )
                    ])
                ])
            )
        
        return html.Div(content)
    
    def _render_results(self, session: QuizSession) -> dbc.Container:
        """Render quiz results and analytics."""
        progress = session.get_progress()
        
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2("Quiz Complete!", className="text-center mb-4"),
                    
                    # Results summary
                    dbc.Card([
                        dbc.CardHeader("Your Results"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H4(f"{progress['correct_answers']}/{progress['total_questions']}", 
                                            className="text-center"),
                                    html.P("Questions Correct", className="text-center text-muted")
                                ], md=3),
                                dbc.Col([
                                    html.H4(f"{progress['accuracy']:.1%}", className="text-center"),
                                    html.P("Accuracy", className="text-center text-muted")
                                ], md=3),
                                dbc.Col([
                                    html.H4(f"{progress['time_elapsed']:.0f}s", className="text-center"),
                                    html.P("Time Taken", className="text-center text-muted")
                                ], md=3),
                                dbc.Col([
                                    html.H4(f"{len(session.hints_used)}", className="text-center"),
                                    html.P("Hints Used", className="text-center text-muted")
                                ], md=3)
                            ])
                        ])
                    ], className="mb-4"),
                    
                    # Action buttons
                    dbc.ButtonGroup([
                        dbc.Button("Take Another Quiz", color="primary", href="/"),
                        dbc.Button("View Analytics", color="info", id="analytics-btn")
                    ], className="w-100")
                    
                ], md=8)
            ], justify="center")
        ])
    
    def _render_statistics_panel(self) -> dbc.Card:
        """Render question pool statistics panel."""
        try:
            stats = self.loader.get_pool_statistics()
            
            return dbc.Card([
                dbc.CardHeader("Question Pool Statistics"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H5(stats['total_questions'], className="text-center"),
                            html.P("Total Questions", className="text-center text-muted small")
                        ], md=3),
                        dbc.Col([
                            html.H5(stats['total_categories'], className="text-center"),
                            html.P("Categories", className="text-center text-muted small")
                        ], md=3),
                        dbc.Col([
                            html.H5(stats['total_hashtags'], className="text-center"),
                            html.P("Hashtags", className="text-center text-muted small")
                        ], md=3),
                        dbc.Col([
                            html.H5(len(stats['by_type']), className="text-center"),
                            html.P("Question Types", className="text-center text-muted small")
                        ], md=3)
                    ])
                ])
            ])
            
        except Exception as e:
            logger.error(f"Error rendering statistics: {e}")
            return dbc.Card([
                dbc.CardBody("Statistics unavailable")
            ])
    
    def _render_error(self, message: str) -> dbc.Container:
        """Render error message."""
        return dbc.Container([
            dbc.Alert([
                html.H4("Error", className="alert-heading"),
                html.P(message)
            ], color="danger")
        ])
    
    def _generate_feedback(self, question: Dict[str, Any], user_answer: Any, correct: bool) -> html.Div:
        """Generate feedback for submitted answer."""
        feedback_content = [
            html.H5("✓ Correct!" if correct else "✗ Incorrect", 
                   className="text-success" if correct else "text-danger")
        ]
        
        # Show correct answer if wrong
        if not correct:
            feedback_content.append(
                html.P(f"The correct answer is: {self._format_correct_answer(question)}")
            )
        
        # Show explanation if available
        if question.get('explanation'):
            feedback_content.extend([
                html.Hr(),
                html.P("Explanation:", className="font-weight-bold"),
                html.P(question['explanation'])
            ])
        
        return html.Div(feedback_content)
    
    def _format_correct_answer(self, question: Dict[str, Any]) -> str:
        """Format correct answer for display."""
        question_type = question['type']
        answer = question['answer']
        
        if question_type == 'multiple_choice':
            choices = question['choices']
            return f"{choices[answer]} (option {answer + 1})"
        elif question_type == 'reorder':
            return " → ".join(question['reorder'])
        elif question_type == 'matching':
            pairs = question['matching']['pairs']
            left = question['matching']['left']
            right = question['matching']['right']
            return ", ".join([f"{left[l]} → {right[r]}" for l, r in pairs])
        else:
            return str(answer)
    
    @monitor_resources
    def run(self, **kwargs) -> None:
        """Run the quiz application server."""
        logger.info(f"Starting Quiz Application on {self.host}:{self.port}")
        
        try:
            self.app.run_server(
                host=self.host,
                port=self.port,
                debug=self.debug,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Failed to start quiz application: {e}")
            raise


# Main application instance
quiz_app = QuizApp()


def main():
    """Main entry point for quiz application."""
    logger.info("Starting Interactive Quiz System")
    
    try:
        # Initialize application
        quiz_app.initialize({})
        
        # Run application server
        quiz_app.run()
        
    except KeyboardInterrupt:
        logger.info("Quiz application stopped by user")
    except Exception as e:
        logger.error(f"Quiz application failed: {e}")
        raise
    finally:
        # Cleanup
        try:
            quiz_app.cleanup()
        except:
            pass


if __name__ == "__main__":
    main()