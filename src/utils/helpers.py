"""
Helper utility functions
"""
import os
from typing import Tuple


def format_duration(seconds: float) -> str:
    """Format duration in seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human readable format"""
    size_mb = round(size_bytes / (1024 * 1024), 2)
    return f"{size_mb} MB"


def get_file_info(file_path: str) -> Tuple[str, str, int]:
    """Get basic file information"""
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1]
    file_size = os.path.getsize(file_path)
    return file_name, file_ext, file_size


def create_progress_bar(progress: float, width: int = 20) -> str:
    """Create ASCII progress bar"""
    filled = int(progress // (100 / width))
    return "█" * filled + "░" * (width - filled)
