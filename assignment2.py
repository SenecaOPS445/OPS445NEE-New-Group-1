#!/usr/bin/env python3

import shutil
import os
import argparse
from datetime import datetime
import json

class BackupTimer:
    """
    Used to create timestamps on backups as well as time taken to create backup operation metadata records.
    """
    def __init__(self):
        self.start_time = datetime.now()
    
    def get_timestamp(self):
        """Return current timestamp in YYYYMMDD_HHMMSS format"""
        return self.start_time.strftime("%Y%m%d_%H%M%S")
    
    def get_iso_timestamp(self):
        """Return ISO 8601 formatted timestamp"""
        return self.start_time.isoformat()
    
    def elapsed(self):
        """Return elapsed time in seconds"""
        return (datetime.now() - self.start_time).total_seconds()

def check_disk_space(source, destination, buffer=1.2):
    """Verify sufficient space exists for backup"""
    try:
        # Calculate source size
        if os.path.isfile(source):
            needed = os.path.getsize(source)
        else:
            needed = sum(os.path.getsize(os.path.join(dirpath, f)) 
                     for dirpath, _, files in os.walk(source) 
                     for f in files)
        
        # Add buffer
        needed *= buffer
        
        # Check available space
        free = shutil.disk_usage(os.path.dirname(destination)).free
        
        if free > needed:
            return True
            
        # Convert to GB for readable output
        needed_gb = needed / (1024**3)
        free_gb = free / (1024**3)
        
        print(f"Not enough space! Need {needed_gb:.1f}GB, only {free_gb:.1f}GB free")
        return False
        
    except Exception as e:
        print(f"Error checking space: {e}")
        return False

def valid_path (path):
    """
    Returns True if the path is valid/exists, 
    prints error/help message and exits the program otherwise.
    """
    if os.path.exists(path):
        return True
    else:
        print(f"[{datetime.now().isoformat()}] Error: Source path {path} does not exist! Please check that you entered the path correctly.")
        exit() # Immediately exit program if the path doesn't exist.

def backup_info(source_path, backup_path, timer):
    """
    Creates metadata file for a given backup operation. 
    File is dropped in the backup folder.
    """
    # timer = BackupTimer() # Timer object for tracking time stats.
     # Create timestamped backup path
    backup_name = f"{os.path.basename(source_path)}_{timer.get_timestamp()}" # Creates a timestamped name for the backup folder/file.
    full_backup_path = os.path.join(backup_path, backup_name) # Full backup path needs to include the created backup file name.

    if os.path.isdir(source_path):
        operation = "directory" # Track backup type for metadata.
    else:
        operation = "file" # Track backup type for metadata.

    # Create metadata
    metadata = {
        "timestamp": timer.get_iso_timestamp(),
        "source": source_path,
        "backup_path": full_backup_path,
        "operation": operation,
        "duration_sec": timer.elapsed()
    }
    
    with open(f"{full_backup_path}.meta", "w") as f: # Drop file containing backup operation stats with the backup directory.
        json.dump(metadata, f, indent=2)


# Function that creates a backup of a specified file/directory
def create_backup(source_path, backup_path):
    # A check to see if the source exists
    valid_path(source_path)
    
    # Create timestamped backup path
    timer = BackupTimer()
    backup_name = f"{os.path.basename(source_path)}_{timer.get_timestamp()}" # Creates a timestamped name for the backup folder/file.
    full_backup_path = os.path.join(backup_path, backup_name) # Full backup path needs to include the created backup file name.
    
    # Check disk space.
    if not check_disk_space(source_path, full_backup_path): # Prevent backup if there is not enough disk space.
        print(f"[{timer.get_iso_timestamp()}] Backup aborted - insufficient space")
        return False
    
    # If the source is a valid directory then it backsup
    if os.path.isdir(source_path):
        # Create the backup by copying the directory to the backup location
        shutil.copytree(source_path, full_backup_path)
        print(f"[{timer.get_iso_timestamp()}] Backup successful ({timer.elapsed():.1f}s)") # Confirmation of successful backup.
        print(f"Directory backup created at: {full_backup_path}")
    
    # If the source is a file then it backsup
    elif os.path.isfile(source_path):
        # Create the backup by copying the file to the backup location
        shutil.copy2(source_path, full_backup_path)
        print(f"[{timer.get_iso_timestamp()}] Backup successful ({timer.elapsed():.1f}s)") # Confirmation of successful backup.
        print(f"File backup created at: {full_backup_path}")

    backup_info(source_path, backup_path, timer)


#Function that restores a backup from the specified path
def restore_backup(backup_path, restore_path):
    # Check if backup exists
    valid_path(backup_path)

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
    try:
        if os.path.isdir(backup_path):
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
    except:
        print(f"Error: unable to restore backup to {restore_path}. Please check that the path your are restoring to is valid.")
        return False

# Backup specified file/directory with compression
def compress_backup(source_path, backup_path, format):
    valid_path(source_path)
    
    # Create timestamped backup path
    timer = BackupTimer()
    backup_name = f"{os.path.basename(source_path)}_{timer.get_timestamp()}"
    full_backup_path = f"{os.path.join(backup_path, backup_name)}"

    # Check disk space
    if not check_disk_space(source_path, full_backup_path, buffer=1.5):
        print(f"[{timer.get_iso_timestamp()}] Backup aborted - insufficient space")
        return False
    
    try: 
        shutil.make_archive(full_backup_path, format, source_path)
        backup_info(source_path, backup_path, timer)
        print(f"[{timer.get_iso_timestamp()}] Compressed backup successful ({timer.elapsed():.1f}s)")
        print(f"Backup created: {full_backup_path}")
    except Exception as e:
        print(f"[{timer.get_iso_timestamp()}] Backup failed: {str(e)}")
        return False



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


 