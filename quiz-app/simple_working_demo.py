#!/usr/bin/env python3
# quiz-app/simple_working_demo.py

"""
Simple Working Demo of the Quiz Dashboard Application.
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

questions = load_questions()
print(f"Loaded {len(questions)} questions")

# Layout
app.layout = dbc.Container([
    html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("🎯 Quiz Dashboard Demo", className="text-center mb-3"),
                html.P("Interactive Quiz System with Framework0 Integration", 
                       className="text-center text-muted mb-4"),
                html.Hr()
            ])
        ]),
        
        # Start Screen
        html.Div(id='main-content', children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H3("🚀 Start Your Quiz", className="mb-0")
                        ]),
                        dbc.CardBody([
                            html.P("Test your knowledge with our interactive quiz system!", 
                                   className="mb-4"),
                            
                            dbc.Button(
                                "Start Demo Quiz",
                                id='start-btn',
                                color="primary",
                                size="lg",
                                className="w-100 mb-3"
                            ),
                            
                            html.Div(id='demo-content')
                        ])
                    ])
                ], md=8)
            ], justify="center"),
            
            # Features showcase
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("📊 Quiz System Features"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H4(str(len(questions)), className="text-primary text-center"),
                                    html.P("Sample Questions", className="text-center text-muted small")
                                ], md=2),
                                dbc.Col([
                                    html.H4("5", className="text-success text-center"),
                                    html.P("Question Types", className="text-center text-muted small")
                                ], md=2),
                                dbc.Col([
                                    html.H4("✨", className="text-warning text-center"),
                                    html.P("LaTeX Support", className="text-center text-muted small")
                                ], md=2),
                                dbc.Col([
                                    html.H4("🧠", className="text-info text-center"),
                                    html.P("Spaced Repetition", className="text-center text-muted small")
                                ], md=2),
                                dbc.Col([
                                    html.H4("📱", className="text-secondary text-center"),
                                    html.P("Mobile Ready", className="text-center text-muted small")
                                ], md=2),
                                dbc.Col([
                                    html.H4("⚡", className="text-danger text-center"),
                                    html.P("Real-time", className="text-center text-muted small")
                                ], md=2)
                            ])
                        ])
                    ])
                ], md=8)
            ], justify="center", className="mt-4")
        ]),
        
        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P("Powered by Framework0 Quiz System", 
                       className="text-center text-muted small mt-4")
            ])
        ])
    ])
], fluid=True, className="py-4")

@app.callback(
    Output('demo-content', 'children'),
    Input('start-btn', 'n_clicks'),
    prevent_initial_call=True
)
def show_demo(n_clicks):
    """Show demo question when start is clicked."""
    if n_clicks and questions:
        sample_q = questions[0]  # Show first question as demo
        
        return [
            html.Hr(),
            html.H5("Demo Question:", className="mt-4 mb-3"),
            
            dbc.Card([
                dbc.CardHeader([
                    dbc.Badge(sample_q['type'].replace('_', ' ').title(), 
                              color="info", className="me-2"),
                    html.Span(f"Difficulty: {sample_q.get('difficulty', 'medium').title()}")
                ]),
                dbc.CardBody([
                    html.H5(sample_q['prompt'], className="mb-3"),
                    
                    # Show choices for MCQ
                    html.Div([
                        dbc.RadioItems(
                            options=[{'label': choice, 'value': i} 
                                   for i, choice in enumerate(sample_q.get('choices', []))],
                            id='demo-answer',
                            className="mb-3"
                        ) if sample_q['type'] == 'multiple_choice' else html.Div([
                            html.P("This demonstrates other question types:", className="mb-2"),
                            html.Ul([
                                html.Li("True/False questions"),
                                html.Li("Fill-in-the-blank with LaTeX support"),
                                html.Li("Drag-and-drop reordering"),
                                html.Li("Matching pairs")
                            ])
                        ])
                    ]),
                    
                    dbc.Button(
                        "Submit Demo Answer",
                        id='submit-demo-btn',
                        color="success",
                        className="me-2"
                    ),
                    
                    html.Div(id='demo-feedback', className="mt-3")
                ])
            ])
        ]
    return html.Div()

@app.callback(
    Output('demo-feedback', 'children'),
    Input('submit-demo-btn', 'n_clicks'),
    State('demo-answer', 'value'),
    prevent_initial_call=True
)
def show_demo_feedback(n_clicks, answer):
    """Show demo feedback."""
    if n_clicks:
        sample_q = questions[0]
        correct = answer == sample_q.get('answer', 0) if answer is not None else False
        
        return dbc.Alert([
            html.H5("✅ Demo Feedback" if correct else "📚 Demo Feedback", 
                   className="mb-2"),
            html.P("Correct! Well done!" if correct else "This is demo feedback. In the full system:"),
            html.Ul([
                html.Li("Answers are evaluated in real-time"),
                html.Li("Detailed explanations are provided"),
                html.Li("Progress is tracked with spaced repetition"),
                html.Li("Performance analytics are generated"),
                html.Li("Adaptive difficulty adjustment")
            ]),
            html.P("The Framework0 integration provides robust error handling, "
                   "logging, and component lifecycle management."),
            dbc.Button("🔄 Try Another Demo", id='reset-demo-btn', 
                      color="primary", outline=True, size="sm", className="mt-2")
        ], color="success" if correct else "info")
    return html.Div()

@app.callback(
    Output('demo-content', 'children', allow_duplicate=True),
    Input('reset-demo-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_demo(n_clicks):
    """Reset demo to show different question."""
    if n_clicks and len(questions) > 1:
        # Show a different question
        sample_q = random.choice(questions[1:3])
        
        return [
            html.Hr(),
            html.H5("Another Demo Question:", className="mt-4 mb-3"),
            
            dbc.Card([
                dbc.CardHeader([
                    dbc.Badge(sample_q['type'].replace('_', ' ').title(), 
                              color="primary", className="me-2"),
                    html.Span(f"Difficulty: {sample_q.get('difficulty', 'medium').title()}")
                ]),
                dbc.CardBody([
                    html.H5(sample_q['prompt'], className="mb-3"),
                    
                    # Show different input based on type
                    html.Div([
                        dbc.RadioItems(
                            options=[{'label': 'True', 'value': True}, {'label': 'False', 'value': False}],
                            id='demo-answer',
                            className="mb-3"
                        ) if sample_q['type'] == 'true_false' 
                        else dbc.Input(placeholder="Enter your answer...", id='demo-text-answer', className="mb-3")
                        if sample_q['type'] == 'fill_blank'
                        else html.P("This question type demonstrates the system's flexibility in handling various formats.")
                    ]),
                    
                    dbc.Button(
                        "Submit Demo Answer",
                        id='submit-demo-btn',
                        color="success"
                    )
                ])
            ])
        ]
    return html.Div()

if __name__ == '__main__':
    print("🚀 Starting Quiz Dashboard Demo...")
    print(f"📚 Loaded {len(questions)} sample questions")
    print("🌐 Open http://127.0.0.1:8050 in your browser")
    print("\n✨ Demo Features:")
    print("   • Interactive question display")
    print("   • Multiple question types")
    print("   • Responsive Bootstrap design")
    print("   • Real-time feedback")
    print("   • Framework0 architecture integration")
    print("\nPress Ctrl+C to stop")
    
    try:
        app.run(debug=False, port=8050, host='0.0.0.0')
    except KeyboardInterrupt:
        print("\n👋 Demo stopped")