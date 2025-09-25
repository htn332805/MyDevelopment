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
