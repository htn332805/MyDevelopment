# analysis/charting.py

"""
Data Visualization Utilities for Framework0.

This module provides functions to create a variety of static and interactive charts
using Matplotlib, Seaborn, and Plotly. It aims to standardize chart creation across
Framework0, ensuring consistency and reusability.

Features:
- `plot_line`: Creates a line chart.
- `plot_bar`: Creates a bar chart.
- `plot_scatter`: Creates a scatter plot.
- `plot_histogram`: Creates a histogram.
- `plot_heatmap`: Creates a heatmap.
- `plot_interactive`: Creates an interactive chart using Plotly.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import numpy as np

# Set Seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")

def plot_line(data: pd.DataFrame, x: str, y: str, title: str = "Line Chart", xlabel: str = "X-axis", ylabel: str = "Y-axis"):
    """
    Creates a line chart using Matplotlib and Seaborn.

    Args:
        data (pd.DataFrame): The data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        title (str): The title of the chart.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x=x, y=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_bar(data: pd.DataFrame, x: str, y: str, title: str = "Bar Chart", xlabel: str = "X-axis", ylabel: str = "Y-axis"):
    """
    Creates a bar chart using Matplotlib and Seaborn.

    Args:
        data (pd.DataFrame): The data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        title (str): The title of the chart.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x=x, y=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_scatter(data: pd.DataFrame, x: str, y: str, title: str = "Scatter Plot", xlabel: str = "X-axis", ylabel: str = "Y-axis"):
    """
    Creates a scatter plot using Matplotlib and Seaborn.

    Args:
        data (pd.DataFrame): The data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        title (str): The title of the chart.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=x, y=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_histogram(data: pd.DataFrame, column: str, bins: int = 30, title: str = "Histogram"):
    """
    Creates a histogram using Matplotlib and Seaborn.

    Args:
        data (pd.DataFrame): The data to plot.
        column (str): The column name for the histogram.
        bins (int): Number of histogram bins.
        title (str): The title of the chart.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x=column, bins=bins)
    plt.title(title)
    plt.show()

def plot_heatmap(data: pd.DataFrame, title: str = "Heatmap"):
    """
    Creates a heatmap using Seaborn.

    Args:
        data (pd.DataFrame): The data to plot (should be numeric).
        title (str): The title of the chart.

    Returns:
        None
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, annot=True, cmap="viridis")
    plt.title(title)
    plt.show()

def plot_interactive(data: pd.DataFrame, x: str, y: str, chart_type: str = "scatter", title: str = "Interactive Chart"):
    """
    Creates an interactive chart using Plotly.

    Args:
        data (pd.DataFrame): The data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        chart_type (str): Type of chart ('scatter', 'line', 'bar').
        title (str): The title of the chart.

    Returns:
        None
    """
    if chart_type == "scatter":
        fig = px.scatter(data, x=x, y=y, title=title)
    elif chart_type == "line":
        fig = px.line(data, x=x, y=y, title=title)
    elif chart_type == "bar":
        fig = px.bar(data, x=x, y=y, title=title)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
    
    fig.show()
