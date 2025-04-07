#!/usr/bin/env python3
"""
Date/Time Tracker Module

"""


from datetime import datetime
import time
import json
import os

class BackupTimer:
    def __init__(self):
        """Initialize timer for operation duration tracking"""
        self.start_time = time.time()
    
    def get_timestamp(self, format="%Y%m%d_%H%M%S"):
        """Get current timestamp in specified format"""
        return datetime.now().strftime(format)
    
    def get_iso_timestamp(self):
        """Get ISO 8601 formatted timestamp with timezone"""
        return datetime.now().isoformat()
    
    def elapsed_seconds(self):
        """Get elapsed time in seconds since timer start"""
        return time.time() - self.start_time
    
    def formatted_duration(self):
        """Get human-readable duration string"""
        duration = self.elapsed_seconds()
        if duration < 60:
            return f"{duration:.2f} seconds"
        minutes, seconds = divmod(duration, 60)
        return f"{int(minutes)}m {seconds:.1f}s"
    
    def generate_metadata(self, source, destination, operation_type):
        """Create standardized backup metadata"""
        return {
            "timestamp": self.get_iso_timestamp(),
            "source_path": os.path.abspath(source),
            "backup_path": os.path.abspath(destination),
            "operation": operation_type,
            "duration_sec": self.elapsed_seconds(),
            "system": os.uname().nodename
        }
    
    def save_metadata(self, metadata, filepath):
        """Save metadata to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)