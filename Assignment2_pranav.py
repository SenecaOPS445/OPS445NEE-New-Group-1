#!/usr/bin/env python3

import shutil
import os
import argparse
from datetime import datetime
import json


class BackupTimer:
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


def valid_path(path):
    """Validate path exists with error handling"""
    if os.path.exists(path):
        return True
    print(f"[{datetime.now().isoformat()}] Error: Path '{path}' doesn't exist")
    return False

def create_backup(source_path, backup_path):
    """Create timestamped backup with space check"""
    timer = BackupTimer()
    
    if not valid_path(source_path):
        return False

    # Create timestamped backup path
    backup_name = f"{os.path.basename(source_path)}_{timer.get_timestamp()}" # Creates a timestamped name for the backup folder/file.
    full_backup_path = os.path.join(backup_path, backup_name) # Full backup path needs to include the created backup file name.

    if not check_disk_space(source_path, full_backup_path): # Prevent backup if there is not enough disk space.
        print(f"[{timer.get_iso_timestamp()}] Backup aborted - insufficient space")
        return False

    try:
        if os.path.isdir(source_path):
            shutil.copytree(source_path, full_backup_path)
            operation = "directory" # Track backup type for metadata.
        else:
            shutil.copy2(source_path, full_backup_path)
            operation = "file" # Track backup type for metadata.

        # Create metadata
        metadata = {
            "timestamp": timer.get_iso_timestamp(),
            "source": source_path,
            "backup_path": full_backup_path,
            "operation": operation,
            "duration_sec": timer.elapsed()
        }
        
        with open(f"{full_backup_path}.meta", "w") as f: # Drop file containing backup operation stats in the backup directory.
            json.dump(metadata, f, indent=2)

        print(f"[{timer.get_iso_timestamp()}] Backup successful ({timer.elapsed():.1f}s)") # Confirmation of successful backup.
        print(f"Backup created: {full_backup_path}")
        return True

    except Exception as e:
        print(f"[{timer.get_iso_timestamp()}] Backup failed: {str(e)}")
        return False

def restore_backup(backup_path, restore_path):
    """Restore backup with verification"""
    timer = BackupTimer()
    
    if not valid_path(backup_path):
        return False

    try:
        # Handle compressed backups
        if any(backup_path.endswith(ext) for ext in ['.zip', '.tar', '.gz', '.bz2', '.xz']):
            print(f"[{timer.get_iso_timestamp()}] Extracting compressed backup...")
            shutil.unpack_archive(backup_path, restore_path)
            print(f"[{timer.get_iso_timestamp()}] Restore completed ({timer.elapsed():.1f}s)")
            return True
            
        # Handle directory/file restoration
        if os.path.isdir(backup_path):
            # Safe directory restore - doesn't overwrite existing
            temp_path = f"{restore_path}.temp"
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)
            shutil.copytree(backup_path, temp_path)
            
            # Finalize restore
            if os.path.exists(restore_path):
                shutil.rmtree(restore_path)
            os.rename(temp_path, restore_path)
        else:
            # Safe file restore
            os.makedirs(os.path.dirname(restore_path), exist_ok=True)
            temp_path = f"{restore_path}.temp"
            shutil.copy2(backup_path, temp_path)
            if os.path.exists(restore_path):
                os.remove(restore_path)
            os.rename(temp_path, restore_path)

        print(f"[{timer.get_iso_timestamp()}] Restore completed ({timer.elapsed():.1f}s)")
        return True

    except Exception as e:
        print(f"[{timer.get_iso_timestamp()}] Restore failed: {str(e)}")
        return False

def compress_backup(source_path, backup_path, format):
    """Create compressed backup with space check"""
    timer = BackupTimer()
    
    if not valid_path(source_path):
        return False

    # Create timestamped backup path
    backup_name = f"{os.path.basename(source_path)}_{timer.get_timestamp()}"
    full_backup_path = f"{os.path.join(backup_path, backup_name)}.{format}"

    if not check_disk_space(source_path, full_backup_path, buffer=1.5):
        print(f"[{timer.get_iso_timestamp()}] Backup aborted - insufficient space")
        return False

    try:
        shutil.make_archive(
            os.path.join(backup_path, backup_name),
            format,
            root_dir=os.path.dirname(source_path),
            base_dir=os.path.basename(source_path)
        )

        # Create metadata
        metadata = {
            "timestamp": timer.get_iso_timestamp(),
            "source": source_path,
            "backup_path": full_backup_path,
            "compression": format,
            "duration_sec": timer.elapsed()
        }
        
        with open(f"{full_backup_path}.meta", "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"[{timer.get_iso_timestamp()}] Compressed backup successful ({timer.elapsed():.1f}s)")
        print(f"Backup created: {full_backup_path}")
        return True

    except Exception as e:
        print(f"[{timer.get_iso_timestamp()}] Backup failed: {str(e)}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup and restore tool with time tracking")
    parser.add_argument("source", help="Path to source file/directory")
    parser.add_argument("destination", help="Backup destination directory")
    parser.add_argument("-f", "--compression_format", 
                       choices=['zip', 'tar', 'gztar', 'bztar', 'xztar'],
                       help="Compression format (default: none)")
    parser.add_argument("-r", "--restore", action="store_true",
                       help="Restore backup instead of creating one")
    parser.add_argument("--info", action="store_true",
                       help="Show backup info only (not implemented)")

    args = parser.parse_args()

    if args.restore:
        restore_backup(args.source, args.destination)
    elif args.compression_format:
        compress_backup(args.source, args.destination, args.compression_format)
    else:
        create_backup(args.source, args.destination)