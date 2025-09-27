""" 
Automation module for SikuliX integration with a function to click on a image then return 1 if success and 0 if unsuccessful.

This module provides cross-platform GUI automation using SikuliX image recognition.
"""
from typing import Union  # Type hints for Union return types
from sikuli import Sikuli  # SikuliX library for GUI automation

def click_image(image_path: str) -> int:
    # Click on an image element if found on screen and return success status
    """Click on an image element if found on screen and return success status."""
    sikuli = Sikuli()  # Create SikuliX automation instance
    if sikuli.click(image_path):  # Attempt to click on image if found
        return 1  # Return success code
    return 0  # Return failure code if image not found or click failed
