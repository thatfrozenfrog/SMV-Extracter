"""
Custom logging utilities for the application
"""
import tkinter as tk
from typing import Callable, Optional


class UILogger:
    """Logger that outputs to a tkinter Text widget"""
    
    def __init__(self, text_widget: tk.Text, progress_bar: Optional[tk.Widget] = None):
        self.text_widget = text_widget
        self.progress_bar = progress_bar
    
    def log_message(self, message: str):
        """Add a message to the logging text area"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"{message}\n")
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear the logging text area"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def update_progress(self, current: int, total: int, message: str = ""):
        """Update the progress bar and optionally log a message"""
        if self.progress_bar and total > 0:
            progress = (current / total) * 100
            self.progress_bar['value'] = progress
            if message:
                self.log_message(f"{message} ({current}/{total} - {progress:.1f}%)")


class YTDLPLogger:
    """Custom logger class to capture yt-dlp output"""
    
    def __init__(self, log_func: Callable[[str], None]):
        self.log_func = log_func
    
    def debug(self, msg: str):
        if msg.startswith('[debug]'):
            return  
        self.log_func(f"[DEBUG] {msg}")
    
    def info(self, msg: str):
        self.log_func(f"[INFO] {msg}")
    
    def warning(self, msg: str):
        self.log_func(f"[WARNING] {msg}")
    
    def error(self, msg: str):
        self.log_func(f"[ERROR] {msg}")
