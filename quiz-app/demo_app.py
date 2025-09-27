#!/usr/bin/env python3
# quiz-app/demo_app.py

"""
Demo launcher for the Quiz Dashboard Application.

This simplified demo shows the quiz system working without all Framework0 dependencies.
"""

import os
import sys
import json
import uuid
import sqlite3
import time
import random
from pathlib import Path
from datetime import datetime

# Dash imports
import dash
from dash import dcc, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Simple session storage (in production would use Redis or database)
quiz_sessions = {}

def create_database():
    """Create SQLite database for demo."""
    db_path = Path("data/db/demo.sqlite")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY,
            question_id TEXT,
            user_answer TEXT,
            correct INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    return str(db_path)

def load_questions():
    """Load sample questions."""
    questions_file = Path("data/questions/sample_questions.json")
    if not questions_file.exists():
        return []
    
    with open(questions_file, 'r') as f:
        return json.load(f)

def evaluate_answer(question, answer):
    """Evaluate if answer is correct."""
    q_type = question['type']
    correct_answer = question['answer']
    
    try:
        if q_type == 'multiple_choice':
            return int(answer) == correct_answer
        elif q_type == 'true_false':
            return bool(answer) == correct_answer
        elif q_type == 'fill_blank':
            if isinstance(correct_answer, list):
                answer_str = str(answer).strip().lower()
                return any(answer_str == str(acc).strip().lower() for acc in correct_answer)
            else:
                return str(answer).strip().lower() == str(correct_answer).strip().lower()
        return False
    except:
        return False

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Quiz Dashboard Demo - Framework0"

# Create database
db_path = create_database()

# Load questions
questions = load_questions()
print(f"Loaded {len(questions)} questions")

# App layout
app.layout = dbc.Container([
    dcc.Store(id='session-store'),
    dcc.Store(id='current-question-store'),
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🎯 Quiz Dashboard Demo", className="text-center mb-4"),
            html.P("Interactive Quiz System with Framework0 Integration", 
                   className="text-center text-muted mb-4"),
            html.Hr()
        ])
    ]),
    
    # Main content
    html.Div(id='main-content'),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Powered by Framework0 Quiz System", 
                   className="text-center text-muted small mt-4")
        ])
    ])
], fluid=True, className="py-4")

@app.callback(
    Output('main-content', 'children'),
    [Input('session-store', 'data')]
)
def display_content(session_data):
    """Display quiz content based on session."""
    if not session_data:
        return render_start_screen()
    
    session_id = session_data.get('session_id')
    if session_id not in quiz_sessions:
        return render_start_screen()
    
    session = quiz_sessions[session_id]
    
    if session['completed']:
        return render_results(session)
    else:
        return render_question(session)

@app.callback(
    Output('session-store', 'data'),
    [Input('start-btn', 'n_clicks')],
    [State('num-questions', 'value')]
)
def start_quiz(n_clicks, num_questions):
    """Start a new quiz session."""
    if not n_clicks or not questions:
        return None
    
    # Create new session
    session_id = str(uuid.uuid4())
    num_q = min(num_questions or 5, len(questions))
    selected_questions = random.sample(questions, num_q)
    
    session = {
        'session_id': session_id,
        'questions': selected_questions,
        'current_index': 0,
        'answers': {},
        'scores': {},
        'start_time': time.time(),
        'completed': False
    }
    
    quiz_sessions[session_id] = session
    
    return {'session_id': session_id}

@app.callback(
    [Output('current-question-store', 'data'),
     Output('feedback-modal', 'is_open'),
     Output('feedback-body', 'children')],
    [Input('submit-btn', 'n_clicks')],
    [State('session-store', 'data'),
     State('answer-input', 'value')]
)
def submit_answer(n_clicks, session_data, answer):
    """Handle answer submission."""
    if not n_clicks or not session_data or answer is None:
        return None, False, ""
    
    session_id = session_data['session_id']
    session = quiz_sessions[session_id]
    
    current_q = session['questions'][session['current_index']]
    correct = evaluate_answer(current_q, answer)
    
    # Store answer
    question_id = current_q['question_id']
    session['answers'][question_id] = answer
    session['scores'][question_id] = correct
    
    # Record in database
    try:
        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO attempts (question_id, user_answer, correct) VALUES (?, ?, ?)",
            (question_id, str(answer), int(correct))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")
    
    # Move to next question
    session['current_index'] += 1
    if session['current_index'] >= len(session['questions']):
        session['completed'] = True
    
    # Generate feedback
    feedback = generate_feedback(current_q, answer, correct)
    
    return {'updated': time.time()}, True, feedback

@app.callback(
    Output('feedback-modal', 'is_open', allow_duplicate=True),
    [Input('continue-btn', 'n_clicks')],
    [State('feedback-modal', 'is_open')],
    prevent_initial_call=True
)
def close_feedback(n_clicks, is_open):
    """Close feedback modal."""
    if n_clicks:
        return False
    return is_open

def render_start_screen():
    """Render quiz start screen."""
    return [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H3("🚀 Start Your Quiz", className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.P("Test your knowledge with our interactive quiz system!", 
                               className="card-text mb-4"),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Number of Questions"),
                                dbc.Input(
                                    id='num-questions',
                                    type='number',
                                    value=5,
                                    min=1,
                                    max=len(questions),
                                    step=1,
                                    className="mb-3"
                                )
                            ], md=6)
                        ]),
                        
                        dbc.Button(
                            "Start Quiz",
                            id='start-btn',
                            color="primary",
                            size="lg",
                            className="w-100"
                        )
                    ])
                ])
            ], md=8, lg=6)
        ], justify="center"),
        
        # Stats
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 System Stats"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H4(str(len(questions)), className="text-primary text-center"),
                                html.P("Total Questions", className="text-center text-muted small")
                            ], md=3),
                            dbc.Col([
                                html.H4("5", className="text-success text-center"),
                                html.P("Question Types", className="text-center text-muted small")
                            ], md=3),
                            dbc.Col([
                                html.H4("✨", className="text-warning text-center"),
                                html.P("LaTeX Support", className="text-center text-muted small")
                            ], md=3),
                            dbc.Col([
                                html.H4("🧠", className="text-info text-center"),
                                html.P("Smart Algorithm", className="text-center text-muted small")
                            ], md=3)
                        ])
                    ])
                ])
            ], md=8, lg=6)
        ], justify="center", className="mt-4")
    ]

def render_question(session):
    """Render current question."""
    current_q = session['questions'][session['current_index']]
    progress = ((session['current_index'] + 1) / len(session['questions'])) * 100
    
    return [
        # Progress
        dbc.Row([
            dbc.Col([
                html.H5(f"Question {session['current_index'] + 1} of {len(session['questions'])}"),
                dbc.Progress(value=progress, className="mb-4")
            ])
        ]),
        
        # Question
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Badge(current_q['type'].replace('_', ' ').title(), 
                                color="info", className="me-2"),
                        html.Span(f"Difficulty: {current_q.get('difficulty', 'medium').title()}")
                    ]),
                    dbc.CardBody([
                        html.H4(current_q['prompt'], className="mb-4"),
                        render_question_input(current_q),
                        
                        dbc.ButtonGroup([
                            dbc.Button("Submit Answer", id='submit-btn', color="primary"),
                            dbc.Button("Hint", color="info", outline=True, disabled=True)
                        ], className="w-100 mt-3")
                    ])
                ])
            ], md=10)
        ], justify="center"),
        
        # Feedback Modal
        dbc.Modal([
            dbc.ModalHeader("Answer Feedback"),
            dbc.ModalBody(id='feedback-body'),
            dbc.ModalFooter([
                dbc.Button("Continue", id='continue-btn', color="primary")
            ])
        ], id='feedback-modal', is_open=False)
    ]

def render_question_input(question):
    """Render input for different question types."""
    q_type = question['type']
    
    if q_type == 'multiple_choice':
        choices = question['choices']
        return dbc.RadioItems(
            id='answer-input',
            options=[{'label': choice, 'value': i} for i, choice in enumerate(choices)],
            className="mb-3"
        )
    
    elif q_type == 'true_false':
        return dbc.RadioItems(
            id='answer-input',
            options=[
                {'label': '✓ True', 'value': True},
                {'label': '✗ False', 'value': False}
            ],
            className="mb-3"
        )
    
    elif q_type == 'fill_blank':
        return dbc.Input(
            id='answer-input',
            type='text',
            placeholder="Enter your answer...",
            className="mb-3"
        )
    
    else:
        return dbc.Input(
            id='answer-input',
            type='text',
            placeholder=f"Answer for {q_type} question...",
            className="mb-3"
        )

def render_results(session):
    """Render quiz results."""
    correct_count = sum(session['scores'].values())
    total_questions = len(session['questions'])
    accuracy = correct_count / total_questions if total_questions > 0 else 0
    
    return [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H3("🎉 Quiz Complete!", className="text-center mb-0")
                    ]),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H1(f"{correct_count}/{total_questions}", 
                                        className="text-center text-success"),
                                html.P("Questions Correct", className="text-center text-muted")
                            ], md=4),
                            dbc.Col([
                                html.H1(f"{accuracy:.1%}", className="text-center text-primary"),
                                html.P("Accuracy", className="text-center text-muted")
                            ], md=4),
                            dbc.Col([
                                html.H1("⭐", className="text-center text-warning"),
                                html.P("Great Job!", className="text-center text-muted")
                            ], md=4)
                        ]),
                        
                        html.Hr(),
                        
                        dbc.Button(
                            "Take Another Quiz",
                            color="primary",
                            href="/",
                            className="w-100"
                        )
                    ])
                ])
            ], md=8)
        ], justify="center")
    ]

def generate_feedback(question, answer, correct):
    """Generate answer feedback."""
    feedback = [
        html.H5("✅ Correct!" if correct else "❌ Incorrect", 
               className="text-success" if correct else "text-danger")
    ]
    
    if not correct:
        correct_answer = question['answer']
        if question['type'] == 'multiple_choice':
            correct_text = question['choices'][correct_answer]
            feedback.append(html.P(f"The correct answer is: {correct_text}"))
        else:
            feedback.append(html.P(f"The correct answer is: {correct_answer}"))
    
    if question.get('explanation'):
        feedback.extend([
            html.Hr(),
            html.Strong("Explanation:"),
            html.P(question['explanation'])
        ])
    
    return feedback

if __name__ == '__main__':
    print("🚀 Starting Quiz Dashboard Demo...")
    print(f"📚 Loaded {len(questions)} sample questions")
    print("🌐 Open http://127.0.0.1:8050 in your browser")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, port=8050, host='0.0.0.0')
    except KeyboardInterrupt:
        print("\n👋 Quiz Dashboard Demo stopped")