"""
Input section UI components - URL entry and file browser
"""
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional


class InputSection:
    """Manages URL input and file browser controls"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.url_change_callback: Optional[Callable[[str], None]] = None
        self.download_callback: Optional[Callable[[], None]] = None
        self.cancel_callback: Optional[Callable[[], None]] = None
        self.file_select_callback: Optional[Callable[[str], None]] = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the input section UI"""
        
        self.input_frame = ttk.Frame(self.parent)
        self.input_frame.pack(pady=(30, 10))

        self.url_label = ttk.Label(self.input_frame, text="Paste youtube link: ")
        self.url_label.pack(side="left", padx=(0, 5))

        self.url_entry = ttk.Entry(self.input_frame, width=30)
        self.url_entry.pack(side="left", padx=(0, 5))
        self.url_entry.bind('<KeyRelease>', self._on_url_change)

        self.download_btn = ttk.Button(self.input_frame, text="Download", command=self._on_download)
        self.download_btn.pack(side="left")

        self.cancel_btn = ttk.Button(self.input_frame, text="Cancel", command=self._on_cancel, state="disabled")
        self.cancel_btn.pack(side="left", padx=(5, 0))

        
        self.local_frame = ttk.Frame(self.parent)
        self.local_frame.pack(pady=(10, 2))

        self.or_label = ttk.Label(self.local_frame, text="Or choose local video: ")
        self.or_label.pack(side="left", padx=(0, 5))

        self.file_btn = ttk.Button(self.local_frame, text="Browse...", command=self._on_file_browse)
        self.file_btn.pack(side="left")
    
    def _on_url_change(self, event):
        """Handle URL entry changes"""
        if self.url_change_callback:
            url = self.url_entry.get().strip()
            self.url_change_callback(url)
    
    def _on_download(self):
        """Handle download button click"""
        if self.download_callback:
            self.download_callback()
    
    def _on_cancel(self):
        """Handle cancel button click"""
        if self.cancel_callback:
            self.cancel_callback()
    
    def _on_file_browse(self):
        """Handle file browse button click"""
        file_path = filedialog.askopenfilename(
            title="Select a video file",
            filetypes=[("Video files", "*.mp4;*.mkv;*.avi;*.mov;*.webm"), ("All files", "*.*")]
        )
        if file_path and self.file_select_callback:
            self.file_select_callback(file_path)
    
    def get_url(self) -> str:
        """Get the current URL from the entry"""
        return self.url_entry.get().strip()
    
    def set_download_state(self, downloading: bool):
        """Update button states based on download status"""
        if downloading:
            self.download_btn.config(state="disabled")
            self.cancel_btn.config(state="normal")
        else:
            self.download_btn.config(state="normal")
            self.cancel_btn.config(state="disabled")
    
    def set_callbacks(self, url_change: Callable[[str], None] = None,
                     download: Callable[[], None] = None,
                     cancel: Callable[[], None] = None,
                     file_select: Callable[[str], None] = None):
        """Set callback functions"""
        if url_change:
            self.url_change_callback = url_change
        if download:
            self.download_callback = download
        if cancel:
            self.cancel_callback = cancel
        if file_select:
            self.file_select_callback = file_select
