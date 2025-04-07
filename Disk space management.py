#!/usr/bin/env python3
"""
Disk Space Manager for Backup System
-----------------------------------
Features:
- Verifies sufficient space before backup
- Calculates required space
- Provides user prompts for low space
- Supports automatic cleanup
"""

import shutil
import os
import sys
from datetime import datetime

class DiskSpaceManager:
    def __init__(self, warning_threshold=20, critical_threshold=10):
        """
        Initialize with thresholds (in %)
        - warning_threshold: When to warn about low space (default: 20%)
        - critical_threshold: When to abort operation (default: 10%)
        """
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold

    def get_space_info(self, path):
        """Get disk usage statistics in bytes"""
        try:
            usage = shutil.disk_usage(os.path.abspath(path))
            return {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'free_percent': 100 * usage.free / usage.total
            }
        except Exception as e:
            print(f"[ERROR] Could not check disk space: {str(e)}")
            return None

    def calculate_required_space(self, source_path):
        """Estimate space needed for backup in bytes"""
        if os.path.isfile(source_path):
            return os.path.getsize(source_path)
        
        total_size = 0
        for dirpath, _, filenames in os.walk(source_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size * 1.1  # Add 10% buffer for metadata

    def check_space(self, backup_path, required_bytes):
        """
        Verify sufficient space exists with user prompts
        Returns: True if proceed, False if abort
        """
        space = self.get_space_info(backup_path)
        if not space:
            return False

        free_percent = space['free_percent']
        required_gb = required_bytes / (1024 ** 3)
        free_gb = space['free'] / (1024 ** 3)

        # Critical space check
        if free_percent < self.critical_threshold:
            print(f"CRITICAL: Only {free_percent:.1f}% free space ({free_gb:.1f}GB)")
            return False

        # Warning threshold check
        if free_percent < self.warning_threshold or space['free'] < required_bytes:
            print(f"Warning: Low disk space ({free_percent:.1f}% free, {free_gb:.1f}GB available)")
            print(f"Backup requires: {required_gb:.1f}GB")
            
            # Interactive prompt
            response = input("Proceed with backup? (y/n): ").lower()
            return response == 'y'

        return True

def create_backup(source_path, backup_path):
    """Enhanced backup with disk space checking"""
    space_mgr = DiskSpaceManager()
    
    # Check source exists
    if not os.path.exists(source_path):
        print(f"Error: Source path '{source_path}' doesn't exist")
        return False

    # Calculate required space
    required_space = space_mgr.calculate_required_space(source_path)
    if not space_mgr.check_space(backup_path, required_space):
        print("Backup aborted due to space constraints")
        return False

    # Proceed with backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{os.path.basename(source_path)}_{timestamp}"
    full_backup_path = os.path.join(backup_path, backup_name)

    try:
        if os.path.isdir(source_path):
            shutil.copytree(source_path, full_backup_path)
        else:
            shutil.copy2(source_path, full_backup_path)

        print(f"Backup successful: {full_backup_path}")
        return True

    except Exception as e:
        print(f"Backup failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) != 3:
        print("Usage: python backup.py <source> <backup_destination>")
        sys.exit(1)

    create_backup(sys.argv[1], sys.argv[2])