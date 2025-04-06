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
    parser.add_argument("--info", action="store_true", help="Show backup info only")

    args = parser.parse_args()

    if args.compression_format == None:
        create_backup(args.source, args.destination)
    else:
        compress_backup(args.source, args.destination, args.compression_format)


 