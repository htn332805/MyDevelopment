# visual_recipe_builder/app.py

"""
Main Dash application for Visual Recipe Builder.

This module creates and configures the Dash web application that provides
a Scratch-like interface for building Framework0 automation recipes.
"""

import json
import uuid
from typing import Dict, Any, List, Optional, Tuple

import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from src.core.logger import get_logger
from .blocks import get_block_library, BlockType, Block, BlockInput, InputType
from .recipe_generator import RecipeGenerator, VisualRecipe, VisualStep

# Initialize logger
logger = get_logger(__name__)


def create_visual_recipe_app(debug: bool = False, port: int = 8050) -> dash.Dash:
    """
    Create and configure the Visual Recipe Builder Dash application.
    
    Args:
        debug (bool): Enable debug mode
        port (int): Port to run the application on
        
    Returns:
        dash.Dash: Configured Dash application
    """
    logger.info("Creating Visual Recipe Builder application")
    
    # Initialize components
    block_library = get_block_library()
    recipe_generator = RecipeGenerator(block_library)
    
    # Create Dash app
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    
    # App layout
    app.layout = create_app_layout(block_library)
    
    # Register callbacks
    register_callbacks(app, block_library, recipe_generator)
    
    logger.info(f"Visual Recipe Builder app created, ready to run on port {port}")
    return app


def create_app_layout(block_library) -> html.Div:
    """
    Create the main application layout.
    
    Args:
        block_library: Block library instance
        
    Returns:
        html.Div: Application layout
    """
    return html.Div([
        # Application title
        html.H1("🔧 Visual Recipe Builder", 
                style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Control panel
        html.Div([
            html.H3("Recipe Controls"),
            html.Div([
                html.Label("Recipe Name:"),
                dcc.Input(id='recipe-name', type='text', placeholder='My Recipe', value='Example Recipe'),
                html.Button('New Recipe', id='new-recipe-btn', n_clicks=0, 
                           style={'marginLeft': '10px'}),
                html.Button('Save Recipe', id='save-recipe-btn', n_clicks=0,
                           style={'marginLeft': '10px'}),
                html.Button('Generate YAML', id='generate-yaml-btn', n_clicks=0,
                           style={'marginLeft': '10px'}),
                html.Button('Execute Recipe', id='execute-recipe-btn', n_clicks=0,
                           style={'marginLeft': '10px'})
            ], style={'marginBottom': '20px'})
        ], style={'border': '1px solid #ccc', 'padding': '15px', 'marginBottom': '20px'}),
        
        # Main content area
        html.Div([
            # Left sidebar - Block library
            html.Div([
                html.H3("Block Library"),
                create_block_library_panel(block_library)
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top',
                     'border': '1px solid #ccc', 'padding': '15px', 'height': '600px',
                     'overflowY': 'scroll'}),
            
            # Center canvas - Recipe design area  
            html.Div([
                html.H3("Recipe Canvas"),
                dcc.Graph(
                    id='recipe-canvas',
                    figure=create_empty_canvas(),
                    style={'height': '500px'},
                    config={'displayModeBar': True, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']}
                )
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top',
                     'border': '1px solid #ccc', 'padding': '15px', 'marginLeft': '10px'}),
            
            # Right sidebar - Step properties
            html.Div([
                html.H3("Step Properties"),
                html.Div(id='step-properties-panel',
                        children="Select a step to edit its properties")
            ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top',
                     'border': '1px solid #ccc', 'padding': '15px', 'marginLeft': '10px',
                     'height': '600px', 'overflowY': 'scroll'})
        ]),
        
        # Output areas
        html.Div([
            html.H3("Generated Recipe"),
            html.Pre(id='generated-yaml', 
                    style={'backgroundColor': '#f5f5f5', 'padding': '15px',
                          'border': '1px solid #ccc', 'height': '300px', 'overflowY': 'scroll'})
        ], style={'marginTop': '20px'}),
        
        # Status and logs
        html.Div([
            html.H3("Status & Logs"),
            html.Div(id='status-output', 
                    style={'backgroundColor': '#f9f9f9', 'padding': '10px',
                          'border': '1px solid #ccc', 'height': '150px', 'overflowY': 'scroll'})
        ], style={'marginTop': '20px'}),
        
        # Hidden stores for application state
        dcc.Store(id='current-recipe', data=None),
        dcc.Store(id='selected-step', data=None),
        dcc.Store(id='canvas-clicks', data=0)
    ])


def create_block_library_panel(block_library) -> html.Div:
    """
    Create the block library panel with categorized blocks.
    
    Args:
        block_library: Block library instance
        
    Returns:
        html.Div: Block library panel
    """
    blocks_by_type = {}
    for block_id, block in block_library.get_blocks().items():
        type_name = block.block_type.value
        if type_name not in blocks_by_type:
            blocks_by_type[type_name] = []
        blocks_by_type[type_name].append(block)
    
    # Create accordion-style layout
    panel_children = []
    for block_type, blocks in blocks_by_type.items():
        # Category header
        panel_children.append(
            html.H4(block_type.replace('_', ' ').title(), 
                   style={'marginTop': '15px', 'marginBottom': '10px'})
        )
        
        # Blocks in category
        for block in blocks:
            block_element = html.Div([
                html.Div([
                    html.Span(block.icon, style={'fontSize': '20px', 'marginRight': '8px'}),
                    html.Span(block.name, style={'fontWeight': 'bold'}),
                ]),
                html.Div(block.description, 
                        style={'fontSize': '12px', 'color': '#666', 'marginTop': '2px'})
            ], 
            id={'type': 'block-item', 'index': block.id},
            style={
                'border': '1px solid #ddd',
                'borderRadius': '5px',
                'padding': '8px',
                'margin': '5px 0',
                'cursor': 'pointer',
                'backgroundColor': block.color + '20'  # Add transparency
            })
            panel_children.append(block_element)
    
    return html.Div(panel_children)


def create_empty_canvas() -> go.Figure:
    """Create an empty canvas for recipe design."""
    fig = go.Figure()
    
    # Set up the canvas
    fig.update_layout(
        title="Drag blocks from the library to build your recipe",
        xaxis=dict(range=[0, 10], showgrid=True, gridcolor='lightgray'),
        yaxis=dict(range=[0, 10], showgrid=True, gridcolor='lightgray'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        dragmode='pan'  # Allow panning
    )
    
    return fig


def create_step_properties_panel(step_data: Optional[Dict[str, Any]], 
                               block_library) -> List[html.Div]:
    """
    Create the step properties editing panel.
    
    Args:
        step_data: Selected step data
        block_library: Block library instance
        
    Returns:
        List[html.Div]: Properties panel components
    """
    if not step_data:
        return [html.P("Select a step to edit its properties")]
    
    block = block_library.get_block(step_data['block_id'])
    if not block:
        return [html.P(f"Unknown block type: {step_data['block_id']}")]
    
    components = []
    
    # Step name
    components.append(
        html.Div([
            html.Label("Step Name:"),
            dcc.Input(
                id='step-name-input',
                type='text',
                value=step_data['step_name'],
                style={'width': '100%', 'marginBottom': '10px'}
            )
        ])
    )
    
    # Step parameters
    components.append(html.H4("Parameters:"))
    
    for input_def in block.inputs:
        param_value = step_data['parameters'].get(input_def.name, input_def.default_value)
        
        components.append(html.Div([
            html.Label(f"{input_def.label}:"),
            create_parameter_input(input_def, param_value),
            html.Small(input_def.description, 
                      style={'color': '#666', 'display': 'block', 'marginBottom': '10px'})
        ]))
    
    # Dependencies
    components.append(html.H4("Dependencies:"))
    components.append(
        html.Div([
            html.Label("Depends on steps:"),
            dcc.Dropdown(
                id='step-dependencies',
                options=[],  # Will be populated dynamically
                value=step_data.get('dependencies', []),
                multi=True,
                style={'marginBottom': '10px'}
            )
        ])
    )
    
    return components


def create_parameter_input(input_def: BlockInput, value: Any) -> dcc.Input:
    """Create appropriate input component for parameter type."""
    if input_def.input_type == InputType.TEXT:
        return dcc.Input(
            id={'type': 'param-input', 'param': input_def.name},
            type='text',
            value=value or '',
            placeholder=f"Enter {input_def.label.lower()}",
            style={'width': '100%'}
        )
    elif input_def.input_type == InputType.NUMBER:
        return dcc.Input(
            id={'type': 'param-input', 'param': input_def.name},
            type='number',
            value=value or 0,
            style={'width': '100%'}
        )
    elif input_def.input_type == InputType.BOOLEAN:
        return dcc.Checklist(
            id={'type': 'param-input', 'param': input_def.name},
            options=[{'label': input_def.label, 'value': True}],
            value=[True] if value else [],
            style={'width': '100%'}
        )
    elif input_def.input_type == InputType.OPTION_SELECT:
        return dcc.Dropdown(
            id={'type': 'param-input', 'param': input_def.name},
            options=[{'label': opt, 'value': opt} for opt in (input_def.options or [])],
            value=value,
            style={'width': '100%'}
        )
    elif input_def.input_type == InputType.FILE_PATH:
        return dcc.Input(
            id={'type': 'param-input', 'param': input_def.name},
            type='text',
            value=value or '',
            placeholder="Enter file path",
            style={'width': '100%'}
        )
    else:
        # Default to text input
        return dcc.Input(
            id={'type': 'param-input', 'param': input_def.name},
            type='text',
            value=str(value or ''),
            style={'width': '100%'}
        )


def register_callbacks(app: dash.Dash, block_library, recipe_generator):
    """Register all Dash callbacks."""
    
    @app.callback(
        [Output('current-recipe', 'data'),
         Output('status-output', 'children')],
        [Input('new-recipe-btn', 'n_clicks')],
        [State('recipe-name', 'value')]
    )
    def create_new_recipe(n_clicks, recipe_name):
        """Create a new empty recipe."""
        if n_clicks == 0:
            return None, "Ready to create a new recipe"
        
        if not recipe_name:
            return None, "Please enter a recipe name"
        
        try:
            recipe = recipe_generator.create_visual_recipe(recipe_name)
            recipe_data = recipe_generator.export_visual_recipe(recipe)
            
            status = f"Created new recipe: {recipe_name}"
            logger.info(status)
            return recipe_data, status
            
        except Exception as e:
            error_msg = f"Error creating recipe: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    @app.callback(
        [Output('recipe-canvas', 'figure'),
         Output('step-properties-panel', 'children')],
        [Input('current-recipe', 'data'),
         Input('selected-step', 'data')]
    )
    def update_canvas_and_properties(recipe_data, selected_step):
        """Update the canvas display and properties panel."""
        fig = create_empty_canvas()
        properties = create_step_properties_panel(selected_step, block_library)
        
        if not recipe_data or not recipe_data.get('steps'):
            return fig, properties
        
        try:
            # Add steps to canvas
            x_coords = []
            y_coords = []
            texts = []
            colors = []
            
            for step in recipe_data['steps']:
                block = block_library.get_block(step['block_id'])
                if block:
                    x, y = step['position']
                    x_coords.append(x)
                    y_coords.append(y)
                    texts.append(f"{block.icon}<br>{step['step_name']}")
                    colors.append(block.color)
            
            if x_coords:
                fig.add_trace(go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode='markers+text',
                    text=texts,
                    textposition="middle center",
                    marker=dict(
                        size=80,
                        color=colors,
                        opacity=0.8,
                        line=dict(width=2, color='black')
                    ),
                    hovertemplate='<b>%{text}</b><extra></extra>'
                ))
            
        except Exception as e:
            logger.error(f"Error updating canvas: {e}")
        
        return fig, properties
    
    @app.callback(
        Output('generated-yaml', 'children'),
        [Input('generate-yaml-btn', 'n_clicks')],
        [State('current-recipe', 'data')]
    )
    def generate_yaml(n_clicks, recipe_data):
        """Generate YAML from visual recipe."""
        if n_clicks == 0 or not recipe_data:
            return "Click 'Generate YAML' to see the recipe"
        
        try:
            recipe = recipe_generator.import_visual_recipe(recipe_data)
            yaml_content = recipe_generator.generate_yaml_recipe(recipe)
            return yaml_content
            
        except Exception as e:
            error_msg = f"Error generating YAML: {str(e)}"
            logger.error(error_msg)
            return error_msg


def main():
    """Main entry point for running the application."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Visual Recipe Builder")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--port', type=int, default=8050, help='Port to run on')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run on')
    
    args = parser.parse_args()
    
    # Create and run app
    app = create_visual_recipe_app(debug=args.debug, port=args.port)
    
    logger.info(f"Starting Visual Recipe Builder on http://{args.host}:{args.port}")
    app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == '__main__':
    main()