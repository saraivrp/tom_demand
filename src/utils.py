"""
Utility functions for TOM Demand Management System.
"""

from typing import Dict, List
import hashlib


def calculate_file_checksum(filepath: str) -> str:
    """
    Calculate MD5 checksum of a file.

    Args:
        filepath: Path to file

    Returns:
        MD5 checksum as hexadecimal string
    """
    md5_hash = hashlib.md5()

    with open(filepath, 'rb') as f:
        # Read file in chunks to handle large files
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "2m 30s" or "45.2s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
