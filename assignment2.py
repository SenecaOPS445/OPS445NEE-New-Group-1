#!/usr/bin/env python3

import shutil
import os
import argparse

def valid_path (path):
    """
    Returns True if the path is valid/exists, 
    prints error/help message and exits the program otherwise.
    """
    if os.path.exists(path):
        return True
    else:
        print(f"Source path {path} does not exist! Please check that you entered the path correctly.")
        exit()
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

        # if os.path.exists(restore_path): # Commenting out this block for now.
        #     shutil.rmtree(restore_path) # We should change this line, it is dangerous and could cause someone to accidentally delete entire directories.

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

# Backup specified file/directory with compression
def compress_backup(source_path, backup_path, format):
    valid_path(source_path)
    shutil.make_archive(backup_path, format, source_path)


# Example usage
if __name__ == "__main__":
    # Variables for the paths
    parser = argparse.ArgumentParser(description="Backup tool with time tracking")
    parser.add_argument("source", help="Path to source file/directory")
    parser.add_argument("destination", help="Backup destination directory")
    parser.add_argument("--compression_format", "-f", default=None, help="Compression format. Default is no compression.\n"
                        "options: zip, tar, gztar, bztar, xztar")
    parser.add_argument("--restore", "-r", action="store_true", help="restores backup [source] to [destination] instead.")
    parser.add_argument("--info", action="store_true", help="Show backup info only")

    args = parser.parse_args()

    if args.restore == True:
        restore_backup(args.source, args.destination)
    elif args.compression_format == None:
        create_backup(args.source, args.destination)
    else:
        compress_backup(args.source, args.destination, args.compression_format)


 