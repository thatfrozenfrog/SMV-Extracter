"""
Logging section UI components
"""
import tkinter as tk
from tkinter import ttk
from ..utils.logger import UILogger


class LoggingSection:
    """Manages logging display and progress tracking"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.logger: UILogger = None
        self.setup_ui()
        self._setup_logger()
    
    def setup_ui(self):
        """Setup the logging section UI"""
        
        self.logging_frame = ttk.LabelFrame(self.parent, text="Logging", padding=10)

        self.logging_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_text_frame = ttk.Frame(self.logging_frame)
        self.log_text_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(self.log_text_frame, height=8, wrap=tk.WORD, state=tk.DISABLED, 
                               fg="#f0f0f0", bg="#333333", font=("Arial", 10))
        self.log_scrollbar = ttk.Scrollbar(self.log_text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        self.log_scrollbar.pack(side="right", fill="y")

        
        self.progress_frame = ttk.Frame(self.logging_frame)
        self.progress_frame.pack(fill="x", pady=(10, 0))

        self.progress_label = ttk.Label(self.progress_frame, text="Progress:")
        self.progress_label.pack(anchor="w")

        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill="x", pady=(5, 0))
    
    def _setup_logger(self):
        """Setup the UI logger"""
        self.logger = UILogger(self.log_text, self.progress_bar)
    
    def get_frame(self) -> ttk.Frame:
        """Get the main frame widget"""
        return self.logging_frame
    
    def get_logger(self) -> UILogger:
        """Get the UI logger instance"""
        return self.logger
    
    def log_message(self, message: str):
        """Log a message"""
        self.logger.log_message(message)
    
    def clear_log(self):
        """Clear the log"""
        self.logger.clear_log()
    
    def update_progress(self, value: float):
        """Update progress bar value (0-100)"""
        self.progress_bar.config(value=value)
    
    def reset_progress(self):
        """Reset progress bar to 0"""
        self.progress_bar.config(value=0)
