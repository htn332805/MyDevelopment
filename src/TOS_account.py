# Function to read lines between line start with "Options" and line containing "OVERALL TOTALS" (not located in the first column) in data\overview.csv into the dataframe df_options
from typing import Optional  # Type hints for Optional return types
import pandas as pd  # Pandas for data manipulation and CSV processing


def read_options_overview(file_path: str) -> Optional[pd.DataFrame]:
    # Read options data from CSV file between specific line markers
    """Read options data from CSV file between specific line markers."""

    with open(file_path, "r") as file:  # Open file for reading
        lines = file.readlines()  # Read all lines into list

    start_index = None  # Initialize start marker index
    end_index = None  # Initialize end marker index

    for i, line in enumerate(lines):  # Iterate through lines to find markers
        if line.startswith("Options"):  # Check for start marker line
            start_index = i
        elif "OVERALL TOTALS" in line and not line.startswith(
            "OVERALL TOTALS"
        ):  # Check for end marker
            end_index = i
            break

    if start_index is not None and end_index is not None:  # Verify both markers found
        options_lines = lines[start_index:end_index]  # Extract relevant lines
        from io import (
            StringIO,
        )  # Import StringIO for creating file-like object from string

        options_data = StringIO(
            "".join(options_lines)
        )  # Create file-like object from extracted lines
        df_options = pd.read_csv(options_data)  # Parse CSV data into DataFrame
        return df_options  # Return processed DataFrame
    else:
        raise ValueError(
            "Could not find the specified lines in the file."
        )  # Raise error if markers not found
