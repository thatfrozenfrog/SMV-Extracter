"""
Main window layout and management
"""
import tkinter as tk
from tkinter import ttk
import sv_ttk
import sys
import platform
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
        
        
        self.center_window()
        
        
        sv_ttk.set_theme("dark")
        
        
        self.root.after(100, self.ensure_window_focus)
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = 900  
        height = 900
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def ensure_window_focus(self):
        """Ensure window gets focus, especially for PyInstaller executables"""
        try:
            
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.update()
            self.root.attributes('-topmost', False)
            self.root.focus_force()
            
            
            if platform.system() == "Windows" and getattr(sys, 'frozen', False):
                try:
                    
                    import ctypes
                    from ctypes import wintypes
                    
                    
                    hwnd = self.root.winfo_id()
                    
                    
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                    ctypes.windll.user32.BringWindowToTop(hwnd)
                    ctypes.windll.user32.ShowWindow(hwnd, 9)  
                except ImportError:
                    pass  
        except Exception:
            pass  
    
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
