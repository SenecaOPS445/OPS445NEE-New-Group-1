#!/usr/bin/env python3

import os
import argparse

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of folder or file to backup")
    args = parser.parse_args()
    ...
