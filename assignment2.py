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

#Function that restores a backup from the specified path
def restore_backup(backup_path, restore_path):
    # Check if backup exists
    if not os.path.exists(backup_path):
        print(f"Backup path {backup_path} does not exist!")
        return False

    # Checking if the backup is a compressed archive
    if any(backup_path.endswith(ext) for ext in ['.zip', '.tar', '.gz', '.bz2', '.xz', '.tgz', '.tbz2', '.txz']):
        try:
            shutil.unpack_archive(backup_path, restore_path)
            print(f"Compressed backup extracted to: {restore_path}")
            return True
        except Exception as e:
            print(f"Failed to extract compressed backup: {e}")
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
    # Variables for the paths
    source_path = "/home/ahassanzadeh-langrud/Desktop/INFO.png"  # Replace with actual source
    backup_path = "/home/ahassanzadeh-langrud/Pictures"          # Replace with your backup directory or file

    # Creates a backup
    create_backup(source_path, backup_path)
