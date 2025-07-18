"""
Main window layout and management
"""
import tkinter as tk
from tkinter import ttk
import sv_ttk
from .input_section import InputSection
from .details_section import DetailsSection
from .logging_section import LoggingSection
from .slicer_section import SlicerSection


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("YouTube Downloader")
        self.root.geometry("900x900")
        self.root.resizable(True, True)
        self.root.minsize(800, 800)
        
        
        sv_ttk.set_theme("dark")
    
    def setup_ui(self):
        """Setup the main UI layout"""
        
        self.input_section = InputSection(self.root)
        
        
        self.details_logging_container = ttk.Frame(self.root)
        self.details_logging_container.pack(pady=(20, 10), padx=20, fill="both", expand=True)
        
        
        self.details_section = DetailsSection(self.details_logging_container)
        self.details_section.get_frame().pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        
        self.logging_section = LoggingSection(self.details_logging_container)
        self.logging_section.get_frame().pack(side="right", fill="both", expand=True)
        
        
        self.slicer_section = SlicerSection(self.root)
        self.slicer_section.get_frame().pack(pady=(10, 10), padx=20, fill="x")
    
    def run(self):
        """Start the main event loop"""
        self.root.mainloop()
    
    def get_root(self):
        """Get the root window"""
        return self.root
