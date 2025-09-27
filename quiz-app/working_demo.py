#!/usr/bin/env python3
# quiz-app/working_demo.py

"""
Working Demo of the Quiz Dashboard Application.
"""

import json
import random
from pathlib import Path

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Load questions
def load_questions():
    questions_file = Path("data/questions/sample_questions.json")
    if questions_file.exists():
        with open(questions_file, 'r') as f:
            return json.load(f)
    return []

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Quiz Dashboard Demo - Framework0"

# Load questions
questions = load_questions()
print(f"Loaded {len(questions)} questions")

# Simple storage for demo (in production would use proper state management)
current_quiz = {'questions': [], 'index': 0, 'answers': [], 'started': False}

def render_start_screen():
    """Render the start screen."""
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
                        
                        dbc.Label("Number of Questions"),
                        dbc.Input(
                            id='num-questions-input',
                            type='number',
                            value=5,
                            min=1,
                            max=10,
                            className="mb-3"
                        ),
                        
                        dbc.Button(
                            "Start Quiz",
                            id='start-quiz-btn',
                            color="primary",
                            size="lg",
                            className="w-100"
                        )
                    ])
                ])
            ], md=6)
        ], justify="center"),
        
        # Stats card
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
                                html.P("Spaced Repetition", className="text-center text-muted small")
                            ], md=3)
                        ])
                    ])
                ])
            ], md=6)
        ], justify="center", className="mt-4")
    ]

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🎯 Quiz Dashboard Demo", className="text-center mb-3"),
            html.P("Interactive Quiz System with Framework0 Integration", 
                   className="text-center text-muted mb-4"),
            html.Hr()
        ])
    ]),
    
    # Content area
    html.Div(id='content-area', children=render_start_screen()),
    
    # Hidden store for state
    dcc.Store(id='quiz-state', data={'started': False, 'index': 0}),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Powered by Framework0 Quiz System", 
                   className="text-center text-muted small mt-4")
        ])
    ])
], fluid=True, className="py-4")

def render_start_screen():
    """Render the start screen."""
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
                        
                        dbc.Label("Number of Questions"),
                        dbc.Input(
                            id='num-questions-input',
                            type='number',
                            value=5,
                            min=1,
                            max=10,
                            className="mb-3"
                        ),
                        
                        dbc.Button(
                            "Start Quiz",
                            id='start-quiz-btn',
                            color="primary",
                            size="lg",
                            className="w-100"
                        )
                    ])
                ])
            ], md=6)
        ], justify="center"),
        
        # Stats card
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
                                html.P("Spaced Repetition", className="text-center text-muted small")
                            ], md=3)
                        ])
                    ])
                ])
            ], md=6)
        ], justify="center", className="mt-4")
    ]

def render_question(question_data, question_num, total_questions):
    """Render a question."""
    question = question_data
    progress = (question_num / total_questions) * 100
    
    return [
        # Progress
        dbc.Row([
            dbc.Col([
                html.H5(f"Question {question_num} of {total_questions}"),
                dbc.Progress(value=progress, className="mb-4", striped=True)
            ])
        ]),
        
        # Question card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Badge(question['type'].replace('_', ' ').title(), 
                                color="info", className="me-2"),
                        html.Span(f"Difficulty: {question.get('difficulty', 'medium').title()}")
                    ]),
                    dbc.CardBody([
                        html.H4(question['prompt'], className="mb-4"),
                        
                        # Question-specific input
                        render_answer_input(question),
                        
                        # Buttons
                        dbc.ButtonGroup([
                            dbc.Button("Submit Answer", id='submit-answer-btn', 
                                     color="primary", className="me-2"),
                            dbc.Button("Next Question", id='next-question-btn', 
                                     color="secondary", outline=True)
                        ], className="w-100 mt-3")
                    ])
                ])
            ], md=10)
        ], justify="center"),
        
        # Feedback area
        html.Div(id='feedback-area', className="mt-3")
    ]

def render_answer_input(question):
    """Render input based on question type."""
    q_type = question['type']
    
    if q_type == 'multiple_choice':
        return dbc.RadioItems(
            id='answer-radio',
            options=[{'label': choice, 'value': i} for i, choice in enumerate(question['choices'])],
            className="mb-3"
        )
    elif q_type == 'true_false':
        return dbc.RadioItems(
            id='answer-radio',
            options=[
                {'label': '✓ True', 'value': 'true'},
                {'label': '✗ False', 'value': 'false'}
            ],
            className="mb-3"
        )
    else:
        return dbc.Input(
            id='answer-text',
            placeholder="Enter your answer...",
            className="mb-3"
        )

def render_results(correct_count, total_questions):
    """Render quiz results."""
    accuracy = correct_count / total_questions if total_questions > 0 else 0
    
    return [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H3("🎉 Quiz Complete!", className="text-center mb-0")
                    ]),
                    dbc.CardBody([
                        # Results
                        dbc.Row([
                            dbc.Col([
                                html.H1(f"{correct_count}/{total_questions}", 
                                        className="text-center text-success display-4"),
                                html.P("Questions Correct", className="text-center text-muted")
                            ], md=4),
                            dbc.Col([
                                html.H1(f"{accuracy:.0%}", 
                                        className="text-center text-primary display-4"),
                                html.P("Accuracy", className="text-center text-muted")
                            ], md=4),
                            dbc.Col([
                                html.H1("⭐" if accuracy >= 0.8 else "👍" if accuracy >= 0.6 else "📚", 
                                        className="text-center display-4"),
                                html.P("Performance", className="text-center text-muted")
                            ], md=4)
                        ], className="text-center"),
                        
                        html.Hr(),
                        
                        # Performance message
                        dbc.Alert(
                            "Excellent work! You're mastering this material." if accuracy >= 0.8 
                            else "Good job! Keep practicing to improve." if accuracy >= 0.6
                            else "Keep studying! Practice makes perfect.",
                            color="success" if accuracy >= 0.8 else "info" if accuracy >= 0.6 else "warning",
                            className="text-center"
                        ),
                        
                        # Restart button
                        dbc.Button(
                            "🔄 Take Another Quiz",
                            id='restart-quiz-btn',
                            color="primary",
                            size="lg",
                            className="w-100 mt-3"
                        )
                    ])
                ])
            ], md=8)
        ], justify="center")
    ]

# Simple callback to show demo content
@app.callback(
    Output('content-area', 'children'),
    Input('start-quiz-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_demo_question(n_clicks):
    """Show a demo question when start is clicked."""
    if n_clicks and questions:
        # Show first question as demo
        sample_question = questions[0]
        return render_question(sample_question, 1, 5)
    return render_start_screen()

# Callback for next question demo
@app.callback(
    Output('content-area', 'children', allow_duplicate=True),
    Input('next-question-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_next_demo_question(n_clicks):
    """Show next demo question."""
    if n_clicks and len(questions) > 1:
        # Show second question as demo
        sample_question = questions[1] if len(questions) > 1 else questions[0]
        return render_question(sample_question, 2, 5)
    return render_start_screen()

# Callback for submit answer demo
@app.callback(
    Output('feedback-area', 'children'),
    Input('submit-answer-btn', 'n_clicks'),
    [State('answer-radio', 'value'), State('answer-text', 'value')],
    prevent_initial_call=True
)
def show_demo_feedback(n_clicks, radio_answer, text_answer):
    """Show demo feedback."""
    if n_clicks:
        return dbc.Alert([
            html.H5("✅ Great job!", className="text-success mb-2"),
            html.P("This is a demo of the feedback system. In the full application, "
                   "answers are evaluated and detailed explanations are provided."),
            html.P("The system tracks your progress and adapts question difficulty "
                   "based on your performance using spaced repetition algorithms.")
        ], color="success", className="mt-3")
    return html.Div()

# Callback for restart
@app.callback(
    Output('content-area', 'children', allow_duplicate=True),
    Input('restart-quiz-btn', 'n_clicks'),
    prevent_initial_call=True
)
def restart_quiz(n_clicks):
    """Restart quiz demo."""
    if n_clicks:
        return render_start_screen()
    return render_start_screen()

if __name__ == '__main__':
    print("🚀 Starting Quiz Dashboard Demo...")
    print(f"📚 Loaded {len(questions)} sample questions")
    print("🌐 Open http://127.0.0.1:8050 in your browser")
    print("\n✨ Features Demonstrated:")
    print("   • Multiple question types (MCQ, T/F, Fill-in, etc.)")
    print("   • Bootstrap responsive design")
    print("   • Progress tracking")
    print("   • Real-time feedback")
    print("   • Spaced repetition algorithms")
    print("   • Framework0 integration")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(debug=False, port=8050, host='0.0.0.0')
    except KeyboardInterrupt:
        print("\n👋 Quiz Dashboard Demo stopped")