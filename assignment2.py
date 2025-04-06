import shutil
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

# Function that creates a backup of a specified file/directory
def create_backup(source_path, backup_path):
    # A check to see if the source exists
    if not os.path.exists(source_path):
        print(f"Source path {source_path} does not exist!")
        return
    
    # If the source is a valid directory then it backsup and if not it gives an error
    if os.path.isdir(source_path):
        # Create the backup by copying the directory to the backup location
        shutil.copytree(source_path, backup_path)
        print(f"Directory backup created at: {backup_path}")
    
    # If the source is a file then it backsup and if not it gives an error
    elif os.path.isfile(source_path):
        # Create the backup by copying the file to the backup location
        shutil.copy2(source_path, backup_path)
        print(f"File backup created at: {backup_path}")
    else:
        print(f"Invalid source path: {source_path}")


# Example usage
if __name__ == "__main__":
    # Variables for the paths
    source_path = "/home/ahassanzadeh-langrud/Desktop/INFO.png"  # Replace with actual source
    backup_path = "/home/ahassanzadeh-langrud/Pictures"          # Replace with your backup directory or file

    # Creates a backup
    create_backup(source_path, backup_path)

 