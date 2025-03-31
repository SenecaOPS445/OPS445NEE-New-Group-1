#!/usr/bin/env python3

import os

def valid_path (path):
    """
    Returns True if the path is valid/exists, returns False 
    and prints an error message otherwise.
    """
    if os.path.exists(path):
        return True
    else:
        print("The path you chose does not exist. Please check that the path is correct.")
        return False
    ...