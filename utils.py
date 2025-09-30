# utils.py

import os
import json
import logging
from typing import List, Dict, Any

# ============================
# Utility Functions
# ============================

def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Reads a JSON file and returns its content as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e}")
    
    return data

def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """
    Writes a dictionary to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        data (dict): The data to write to the file.

    Raises:
        IOError: If the file cannot be written.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        raise IOError(f"Failed to write to file {file_path}: {e}")

def setup_logger(name: str, log_file: str) -> logging.Logger:
    """
    Sets up a logger that writes to both console and a log file.

    Args:
        name (str): The name of the logger.
        log_file (str): The path to the log file.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

def filter_even_numbers(numbers: List[int]) -> List[int]:
    """
    Filters out the even numbers from a list.

    Args:
        numbers (list): A list of integers.

    Returns:
        list: A list containing only the even numbers.
    """
    return [num for num in numbers if num % 2 == 0]

def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Flattens a nested list into a single list.

    Args:
        nested_list (list): A list of lists.

    Returns:
        list: A flattened list containing all the elements.
    """
    return [item for sublist in nested_list for item in sublist]

def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges two dictionaries into one. If there are overlapping keys, values from dict2 overwrite those from dict1.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.

    Returns:
        dict: A dictionary containing all keys and values from both dict1 and dict2.
    """
    merged = dict1.copy()  # Start with dict1's keys and values
    merged.update(dict2)   # Update with dict2's keys and values
    return merged

def get_file_extension(file_name: str) -> str:
    """
    Returns the file extension from a file name.

    Args:
        file_name (str): The name of the file.

    Returns:
        str: The file extension, including the dot (e.g., '.txt').
    """
    _, ext = os.path.splitext(file_name)
    return ext

def is_palindrome(s: str) -> bool:
    """
    Checks if a string is a palindrome.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    return s == s[::-1]

def calculate_average(numbers: List[float]) -> float:
    """
    Calculates the average of a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        float: The average of the numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("The list is empty.")
    return sum(numbers) / len(numbers)
