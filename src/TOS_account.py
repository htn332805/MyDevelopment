# function to read lines between line start with "Options" and and line containing "OVERALL TOTALS" (not locate in the first column) in data\overview.csv into the dataframe df_options
def read_options_overview(file_path):
    import pandas as pd

    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if line.startswith("Options"):
            start_index = i
        elif "OVERALL TOTALS" in line and not line.startswith("OVERALL TOTALS"):
            end_index = i
            break

    if start_index is not None and end_index is not None:
        options_lines = lines[start_index:end_index]
        from io import StringIO
        options_data = StringIO(''.join(options_lines))
        df_options = pd.read_csv(options_data)
        return df_options
    else:
        raise ValueError("Could not find the specified lines in the file.")
    
