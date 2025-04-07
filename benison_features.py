import shutil
import os
import sys

def restore_backup(backup_path, restore_path):
    """
    Restores a backup from backup_path to restore_path.
    Handles both file and directory backups.
    """
    # Check if backup exists
    if not os.path.exists(backup_path):
        print(f"Backup path {backup_path} does not exist!")
        return False
    
 # Check if the backup is a compressed archive
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

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Restore: python assignment2.py restore <backup> <destination>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "restore":
        if len(sys.argv) != 4:
            print("Error: Restore requires backup and destination paths")
            print("Usage: python assignment2.py restore <backup> <destination>")
            sys.exit(1)
        restore_backup(sys.argv[2], sys.argv[3])

    else:
        print(f"Error: Unknown command '{command}'")
        print("Available commands: backup, restore")
        sys.exit(1)
 