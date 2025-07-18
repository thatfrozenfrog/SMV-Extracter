"""
Slicer section UI components
"""
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk
from typing import Callable, Optional, List, Tuple


class SlicerSection:
    """Manages video slicer controls and preview"""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.duration_change_callback: Optional[Callable[[float], None]] = None
        self.offset_change_callback: Optional[Callable[[float], None]] = None
        self.refresh_preview_callback: Optional[Callable[[], None]] = None
        self.choose_directory_callback: Optional[Callable[[str], None]] = None
        self.cut_video_callback: Optional[Callable[[], None]] = None
        
        self.preview_thumbnails: List[ImageTk.PhotoImage] = []
        self.export_directory: Optional[str] = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the slicer section UI"""
        
        self.slicer_frame = ttk.LabelFrame(self.parent, text="Slicer", padding=10)

        
        self.duration_controls_frame = ttk.Frame(self.slicer_frame)
        self.duration_controls_frame.pack(fill="x", pady=(0, 10))

        
        self.slider_frame = ttk.Frame(self.duration_controls_frame)
        self.slider_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        
        self.slider_label_frame = ttk.Frame(self.slider_frame)
        self.slider_label_frame.pack(fill="x")

        self.duration_slider_label = ttk.Label(self.slider_label_frame, text="Cut duration:")
        self.duration_slider_label.pack(side="left")

        self.duration_value_label = ttk.Label(self.slider_label_frame, text="2.0s")
        self.duration_value_label.pack(side="right")

        
        self.duration_slider = ttk.Scale(self.slider_frame, from_=0.5, to=10.0, orient="horizontal")
        self.duration_slider.pack(fill="x", pady=(5, 0))

        
        self.manual_duration_frame = ttk.Frame(self.duration_controls_frame)
        self.manual_duration_frame.pack(side="right")

        ttk.Label(self.manual_duration_frame, text="Manual:").pack(anchor="w")
        self.duration_entry = ttk.Entry(self.manual_duration_frame, width=8)
        self.duration_entry.pack()
        self.duration_entry.insert(0, "2.0")
        self.duration_entry.bind('<Return>', self._on_manual_duration_change)
        self.duration_entry.bind('<FocusOut>', self._on_manual_duration_change)

        
        self.offset_controls_frame = ttk.Frame(self.slicer_frame)
        self.offset_controls_frame.pack(fill="x", pady=(0, 10))

        
        self.offset_slider_frame = ttk.Frame(self.offset_controls_frame)
        self.offset_slider_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        
        self.offset_label_frame = ttk.Frame(self.offset_slider_frame)
        self.offset_label_frame.pack(fill="x")

        self.offset_slider_label = ttk.Label(self.offset_label_frame, text="Start offset:")
        self.offset_slider_label.pack(side="left")

        self.offset_value_label = ttk.Label(self.offset_label_frame, text="0.0s")
        self.offset_value_label.pack(side="right")

        
        self.offset_slider = ttk.Scale(self.offset_slider_frame, from_=0.0, to=10.0, orient="horizontal")
        self.offset_slider.pack(fill="x", pady=(5, 0))

        
        self.manual_offset_frame = ttk.Frame(self.offset_controls_frame)
        self.manual_offset_frame.pack(side="right")

        ttk.Label(self.manual_offset_frame, text="Manual:").pack(anchor="w")
        self.offset_entry = ttk.Entry(self.manual_offset_frame, width=8)
        self.offset_entry.pack()
        self.offset_entry.insert(0, "0.0")
        self.offset_entry.bind('<Return>', self._on_manual_offset_change)
        self.offset_entry.bind('<FocusOut>', self._on_manual_offset_change)

        
        self.preview_frame = ttk.LabelFrame(self.slicer_frame, text="Preview (6 frames with offset)", padding=5)
        self.preview_frame.pack(fill="both", expand=True, pady=(10, 10))

        
        self.preview_controls_frame = ttk.Frame(self.preview_frame)
        self.preview_controls_frame.pack(fill="x", pady=(0, 5))

        self.refresh_preview_btn = ttk.Button(self.preview_controls_frame, text="Refresh Preview", 
                                            command=self._on_refresh_preview)
        self.refresh_preview_btn.pack(side="left")

        
        self.preview_canvas = tk.Canvas(self.preview_frame, height=120)
        self.preview_scrollbar = ttk.Scrollbar(self.preview_frame, orient="horizontal", 
                                             command=self.preview_canvas.xview)
        self.preview_canvas.configure(xscrollcommand=self.preview_scrollbar.set)
        
        self.preview_inner_frame = ttk.Frame(self.preview_canvas)
        self.preview_canvas.create_window((0, 0), window=self.preview_inner_frame, anchor="nw")
        
        self.preview_canvas.pack(fill="x")
        self.preview_scrollbar.pack(fill="x")

        
        self.cut_controls_frame = ttk.Frame(self.slicer_frame)
        self.cut_controls_frame.pack(fill="x", pady=(10, 0))

        self.export_dir_label = ttk.Label(self.cut_controls_frame, text="Export directory: Not selected", 
                                        wraplength=600)
        self.export_dir_label.pack(anchor="w", pady=(0, 5))

        self.cut_buttons_frame = ttk.Frame(self.cut_controls_frame)
        self.cut_buttons_frame.pack(fill="x")

        self.choose_dir_btn = ttk.Button(self.cut_buttons_frame, text="Choose Directory", 
                                       command=self._on_choose_directory)
        self.choose_dir_btn.pack(side="left")

        self.cut_btn = ttk.Button(self.cut_buttons_frame, text="Cut", command=self._on_cut_video, 
                                state="disabled")
        self.cut_btn.pack(side="left", padx=(10, 0))
        
        
        self.duration_slider.config(command=self._on_duration_change)
        self.duration_slider.set(2.0)  
        self.offset_slider.config(command=self._on_offset_change)
        self.offset_slider.set(0.0)  
    
    def _on_duration_change(self, value):
        """Handle duration slider changes"""
        
        if not hasattr(self, 'duration_entry') or not hasattr(self, 'duration_value_label'):
            return
            
        duration = float(value)
        self.duration_value_label.config(text=f"{duration:.1f}s")
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, f"{duration:.1f}")
        if self.duration_change_callback:
            self.duration_change_callback(duration)
    
    def _on_manual_duration_change(self, event):
        """Handle manual duration entry changes"""
        if not hasattr(self, 'duration_entry') or not hasattr(self, 'duration_slider'):
            return
            
        try:
            duration = float(self.duration_entry.get())
            duration = max(0.1, min(duration, self.duration_slider['to']))  
            self.duration_slider.set(duration)
            self.duration_value_label.config(text=f"{duration:.1f}s")
            if self.duration_change_callback:
                self.duration_change_callback(duration)
        except ValueError:
            
            current_duration = float(self.duration_slider.get())
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, f"{current_duration:.1f}")
    
    def _on_offset_change(self, value):
        """Handle offset slider changes"""
        
        if not hasattr(self, 'offset_entry') or not hasattr(self, 'offset_value_label'):
            return
            
        offset = float(value)
        self.offset_value_label.config(text=f"{offset:.1f}s")
        self.offset_entry.delete(0, tk.END)
        self.offset_entry.insert(0, f"{offset:.1f}")
        if self.offset_change_callback:
            self.offset_change_callback(offset)
    
    def _on_manual_offset_change(self, event):
        """Handle manual offset entry changes"""
        if not hasattr(self, 'offset_entry') or not hasattr(self, 'offset_slider'):
            return
            
        try:
            offset = float(self.offset_entry.get())
            offset = max(0.0, min(offset, self.offset_slider['to']))  
            self.offset_slider.set(offset)
            self.offset_value_label.config(text=f"{offset:.1f}s")
            if self.offset_change_callback:
                self.offset_change_callback(offset)
        except ValueError:
            
            current_offset = float(self.offset_slider.get())
            self.offset_entry.delete(0, tk.END)
            self.offset_entry.insert(0, f"{current_offset:.1f}")
    
    def _on_refresh_preview(self):
        """Handle refresh preview button click"""
        
        self.refresh_preview_btn.config(text="Generating 0.000%", state="disabled")
        if self.refresh_preview_callback:
            self.refresh_preview_callback()
    
    def update_preview_progress(self, progress: float):
        """Update the preview button with generation progress"""
        self.refresh_preview_btn.config(text=f"Generating {progress:.3f}%")
    
    def reset_preview_button(self):
        """Reset the preview button to normal state"""
        self.refresh_preview_btn.config(text="Refresh Preview", state="normal")
    
    def _on_choose_directory(self):
        """Handle choose directory button click"""
        directory = filedialog.askdirectory(title="Choose export directory")
        if directory:
            self.export_directory = directory
            self.export_dir_label.config(text=f"Export directory: {directory}")
            if self.choose_directory_callback:
                self.choose_directory_callback(directory)
    
    def _on_cut_video(self):
        """Handle cut video button click"""
        if self.cut_video_callback:
            self.cut_video_callback()
    
    def get_frame(self) -> ttk.LabelFrame:
        """Get the main frame widget"""
        return self.slicer_frame
    
    def get_duration(self) -> float:
        """Get current duration slider value"""
        return float(self.duration_slider.get())
    
    def get_offset(self) -> float:
        """Get current offset slider value"""
        return float(self.offset_slider.get())
    
    def get_export_directory(self) -> Optional[str]:
        """Get selected export directory"""
        return self.export_directory
    
    def set_duration_range(self, max_duration: float):
        """Set the maximum duration for the slider"""
        self.duration_slider.config(to=max_duration)
    
    def set_offset_range(self, max_offset: float):
        """Set the maximum offset for the slider"""
        self.offset_slider.config(to=max_offset)
    
    def update_cut_button_state(self, enabled: bool):
        """Enable/disable the cut button"""
        state = "normal" if enabled else "disabled"
        self.cut_btn.config(state=state)
    
    def set_cut_button_text(self, text: str):
        """Set the cut button text"""
        self.cut_btn.config(text=text)
    
    def display_previews(self, previews: List[Tuple[ImageTk.PhotoImage, float]]):
        """Display preview thumbnails"""
        self.clear_preview()
        
        for i, (thumbnail, timestamp) in enumerate(previews):
            frame = ttk.Frame(self.preview_inner_frame)
            frame.pack(side="left", padx=2)
            
            label = ttk.Label(frame, image=thumbnail)
            label.pack()
            
            time_label = ttk.Label(frame, text=f"{timestamp:.1f}s", font=("Arial", 8))
            time_label.pack()
            
            
            self.preview_thumbnails.append(thumbnail)
        
        
        self.preview_inner_frame.update_idletasks()
        self.preview_canvas.config(scrollregion=self.preview_canvas.bbox("all"))
    
    def clear_preview(self):
        """Clear all preview thumbnails"""
        for widget in self.preview_inner_frame.winfo_children():
            widget.destroy()
        self.preview_thumbnails.clear()
    
    def set_callbacks(self, duration_change: Optional[Callable[[float], None]] = None,
                     offset_change: Optional[Callable[[float], None]] = None,
                     refresh_preview: Optional[Callable[[], None]] = None,
                     choose_directory: Optional[Callable[[str], None]] = None,
                     cut_video: Optional[Callable[[], None]] = None):
        """Set callback functions"""
        if duration_change:
            self.duration_change_callback = duration_change
        if offset_change:
            self.offset_change_callback = offset_change
        if refresh_preview:
            self.refresh_preview_callback = refresh_preview
        if choose_directory:
            self.choose_directory_callback = choose_directory
        if cut_video:
            self.cut_video_callback = cut_video
