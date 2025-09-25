# analysis/exporter.py

"""
Data Export Utilities for Framework0.

This module provides functions to export data from Pandas DataFrames into various
formats including CSV, Excel, JSON, and HTML. It aims to standardize data export
across Framework0, ensuring consistency and reusability.

Features:
- `export_to_csv(df, filepath, index=False, **kwargs)`: Exports DataFrame to CSV.
- `export_to_excel(df, filepath, index=False, **kwargs)`: Exports DataFrame to Excel.
- `export_to_json(df, filepath, orient='records', **kwargs)`: Exports DataFrame to JSON.
- `export_to_html(df, filepath, **kwargs)`: Exports DataFrame to HTML.
"""

import pandas as pd

def export_to_csv(df: pd.DataFrame, filepath: str, index: bool = False, **kwargs):
    """
    Exports the given DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        filepath (str): The path where the CSV file will be saved.
        index (bool): Whether to write row names (index). Default is False.
        **kwargs: Additional arguments passed to `DataFrame.to_csv()`.

    Returns:
        None
    """
    try:
        df.to_csv(filepath, index=index, **kwargs)
        print(f"✅ Data exported to CSV: {filepath}")
    except Exception as e:
        print(f"❌ Failed to export to CSV: {e}")

def export_to_excel(df: pd.DataFrame, filepath: str, index: bool = False, **kwargs):
    """
    Exports the given DataFrame to an Excel file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        filepath (str): The path where the Excel file will be saved.
        index (bool): Whether to write row names (index). Default is False.
        **kwargs: Additional arguments passed to `DataFrame.to_excel()`.

    Returns:
        None
    """
    try:
        df.to_excel(filepath, index=index, **kwargs)
        print(f"✅ Data exported to Excel: {filepath}")
    except Exception as e:
        print(f"❌ Failed to export to Excel: {e}")

def export_to_json(df: pd.DataFrame, filepath: str, orient: str = 'records', **kwargs):
    """
    Exports the given DataFrame to a JSON file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        filepath (str): The path where the JSON file will be saved.
        orient (str): The format of the JSON string. Default is 'records'.
        **kwargs: Additional arguments passed to `DataFrame.to_json()`.

    Returns:
        None
    """
    try:
        df.to_json(filepath, orient=orient, **kwargs)
        print(f"✅ Data exported to JSON: {filepath}")
    except Exception as e:
        print(f"❌ Failed to export to JSON: {e}")

def export_to_html(df: pd.DataFrame, filepath: str, **kwargs):
    """
    Exports the given DataFrame to an HTML file.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        filepath (str): The path where the HTML file will be saved.
        **kwargs: Additional arguments passed to `DataFrame.to_html()`.

    Returns:
        None
    """
    try:
        df.to_html(filepath, **kwargs)
        print(f"✅ Data exported to HTML: {filepath}")
    except Exception as e:
        print(f"❌ Failed to export to HTML: {e}")
