""" 
automation module for sikulix integration with a function to click on a image then return 1 if success and 0 if unsuccessful

"""
from sikuli import Sikuli

def click_image(image_path):
    sikuli = Sikuli()
    if sikuli.click(image_path):
        return 1
    return 0
