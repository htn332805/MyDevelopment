
from typing import Any, Dict, List, Optional, Union

# src/modules/data_processing/csv_reader.py
from src.core.logger import get_logger

logger = get_logger("csv_reader", debug=True)

def read_csv(file_path: str) -> list:
    # Execute read_csv operation
    """Reads a CSV file and returns list of rows."""
    logger.debug(f"Received input: {file_path}")
    try:
        with open(file_path, "r") as f:
            data = f.readlines()
        logger.debug(f"Returning output: {data}")
        return data
    except Exception as e:
        logger.exception("Failed to read CSV")
        raise
