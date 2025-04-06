import shutil
import os
import sys
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

#Function that restores a backup from the specified path
def restore_backup(backup_path, restore_path):
    # Check if backup exists
    if not os.path.exists(backup_path):
        print(f"Backup path {backup_path} does not exist!")
        return False

    # If restoring a directory
    if os.path.isdir(backup_path):
        # Remove existing directory if it exists
        if os.path.exists(restore_path):
            shutil.rmtree(restore_path)
        shutil.copytree(backup_path, restore_path)
        print(f"Directory restored to: {restore_path}")
        return True

    # If restoring a file
    elif os.path.isfile(backup_path):
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(restore_path), exist_ok=True)
        shutil.copy2(backup_path, restore_path)
        print(f"File restored to: {restore_path}")
        return True

    else:
        print(f"Invalid backup path: {backup_path}")
        return False


# Example usage
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Backup: python assignment2.py backup <source> <destination>")
        print("  Restore: python assignment2.py restore <backup> <destination>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "backup":
        if len(sys.argv) != 4:
            print("Error: Backup requires source and destination paths")
            print("Usage: python assignment2.py backup <source> <destination>")
            sys.exit(1)
        create_backup(sys.argv[2], sys.argv[3])

    elif command == "restore":
        if len(sys.argv) != 4:
            print("Error: Restore requires backup and destination paths")
            print("Usage: python assignment2.py restore <backup> <destination>")
            sys.exit(1)
        restore_backup(sys.argv[2], sys.argv[3])

    else:
        print(f"Error: Unknown command '{command}'")
        print("Available commands: backup, restore")
        sys.exit(1)
 