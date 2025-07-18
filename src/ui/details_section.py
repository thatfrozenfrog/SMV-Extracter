"""
Media details section UI components
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from typing import Optional


class DetailsSection:
    """Manages media details display"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.current_thumbnail: Optional[ImageTk.PhotoImage] = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the details section UI"""
        
        self.details_frame = ttk.LabelFrame(self.parent, text="Media Details", padding=10)
        
        
        self.info_container = ttk.Frame(self.details_frame)
        self.info_container.pack(fill="x")

        
        self.thumbnail_label = ttk.Label(self.info_container, text="No media selected", 
                                       width=20, relief="sunken", anchor="center")
        self.thumbnail_label.pack(side="left", padx=(0, 10))

        
        self.info_frame = ttk.Frame(self.info_container)
        self.info_frame.pack(side="left", fill="both", expand=True)

        
        self.title_label = ttk.Label(self.info_frame, text="Title: -", font=("Arial", 10, "bold"))
        self.title_label.pack(anchor="w")

        self.duration_label = ttk.Label(self.info_frame, text="Duration: -")
        self.duration_label.pack(anchor="w")

        self.size_label = ttk.Label(self.info_frame, text="Size: -")
        self.size_label.pack(anchor="w")

        self.format_label = ttk.Label(self.info_frame, text="Format: -")
        self.format_label.pack(anchor="w")
    
    def get_frame(self) -> ttk.Frame:
        """Get the main frame widget"""
        return self.details_frame
    
    def update_details(self, title: str, duration: str, size: str, format_type: str):
        """Update media details"""
        self.title_label.config(text=f"Title: {title}")
        self.duration_label.config(text=f"Duration: {duration}")
        self.size_label.config(text=f"Size: {size}")
        self.format_label.config(text=f"Format: {format_type}")
    
    def set_thumbnail(self, thumbnail: Optional[ImageTk.PhotoImage]):
        """Set thumbnail image"""
        if thumbnail:
            self.current_thumbnail = thumbnail
            self.thumbnail_label.config(image=self.current_thumbnail, text="")
        else:
            self.thumbnail_label.config(text="No thumbnail\navailable", image="")
    
    def set_placeholder_text(self, text: str):
        """Set placeholder text for thumbnail"""
        self.thumbnail_label.config(text=text, image="")
    
    def reset(self):
        """Reset to default state"""
        self.update_details("-", "-", "-", "-")
        self.set_placeholder_text("No media selected")
