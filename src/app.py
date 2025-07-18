"""
Main application class that coordinates all components
"""
import os
from tkinter import messagebox
from .ui.main_window import MainWindow
from .core.downloader import YouTubeDownloader
from .core.video_processor import VideoProcessor
from .core.thumbnail_manager import ThumbnailManager
from .utils.helpers import format_duration, format_file_size, get_file_info


class SMVExtractorApp:
    """Main application class"""
    
    def __init__(self):
        self.window = MainWindow()
        self.downloader = YouTubeDownloader()
        self.video_processor = VideoProcessor()
        self.thumbnail_manager = ThumbnailManager()
        
        
        self.current_video_path = None
        self.current_video_duration = 0
        
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Setup callbacks between UI components and core functionality"""
        
        self.window.input_section.set_callbacks(
            url_change=self.on_url_change,
            download=self.on_download_video,
            cancel=self.on_cancel_download,
            file_select=self.on_file_selected
        )
        
        
        self.window.slicer_section.set_callbacks(
            duration_change=self.on_duration_change,
            offset_change=self.on_offset_change,
            refresh_preview=self.on_refresh_preview,
            choose_directory=self.on_directory_chosen,
            cut_video=self.on_cut_video
        )
    
    def on_url_change(self, url: str):
        """Handle URL entry changes"""
        if url and ('youtube.com' in url or 'youtu.be' in url):
            
            self.window.get_root().after(1000, lambda: self.get_youtube_info(url))
    
    def get_youtube_info(self, url: str):
        """Get YouTube video information"""
        def on_info_received(info):
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            duration_str = format_duration(duration) if duration else "Unknown"
            
            
            thumbnail_url = None
            if 'thumbnail' in info:
                thumbnail_url = info['thumbnail']
            elif 'thumbnails' in info and info['thumbnails']:
                thumbnails = info['thumbnails']
                thumbnail_url = thumbnails[-1]['url']
            
            size_estimate = "~50-100 MB"
            
            
            self.window.details_section.update_details(title, duration_str, size_estimate, "MP4 (video only)")
            
            
            if thumbnail_url:
                self.thumbnail_manager.download_youtube_thumbnail(
                    thumbnail_url,
                    self.window.details_section.set_thumbnail,
                    lambda: self.window.details_section.set_placeholder_text("YouTube Video\nReady to Download")
                )
        
        def on_error(error):
            messagebox.showerror("Error", f"Could not fetch video info: {error}")
        
        self.downloader.get_video_info(url, on_info_received, on_error)
    
    def on_download_video(self):
        """Handle video download"""
        url = self.window.input_section.get_url()
        if not url:
            self.window.logging_section.log_message("ERROR: Please enter a YouTube URL.")
            return
        
        self.window.input_section.set_download_state(True)
        self.window.logging_section.clear_log()
        
        def on_progress(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                if total > 0:
                    percent = (downloaded / total) * 100
                    speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "Unknown"
                    eta_str = f"{eta}s" if eta else "Unknown"
                    
                    self.window.logging_section.update_progress(percent)
                    self.window.logging_section.log_message(
                        f"Downloading: {percent:.1f}% - Speed: {speed_str} - ETA: {eta_str}"
                    )
            elif d['status'] == 'finished':
                filename = d.get('filename', 'Unknown')
                self.window.logging_section.log_message(f"Download completed: {filename}")
                
                self.window.get_root().after(100, lambda: self.load_video_file(filename))
        
        def on_completion(filename):
            self.window.logging_section.update_progress(100)
            self.window.input_section.set_download_state(False)
        
        def on_error(error):
            self.window.logging_section.log_message(f"ERROR: {error}")
            self.window.logging_section.reset_progress()
            self.window.input_section.set_download_state(False)
        
        def on_log(message):
            self.window.logging_section.log_message(message)
        
        self.downloader.download_video(url, on_progress, on_completion, on_error, on_log)
    
    def on_cancel_download(self):
        """Handle download cancellation"""
        self.downloader.cancel_download()
        self.window.input_section.set_download_state(False)
        self.window.logging_section.log_message("Download cancelled by user")
        self.window.logging_section.reset_progress()
    
    def on_file_selected(self, file_path: str):
        """Handle local file selection"""
        self.load_video_file(file_path)
    
    def load_video_file(self, file_path: str):
        """Load and display video file information"""
        try:
            self.window.logging_section.log_message(f"Loading video file: {os.path.basename(file_path)}")
            
            
            file_name, file_ext, file_size = get_file_info(file_path)
            size_str = format_file_size(file_size)
            
            
            duration, error = self.video_processor.get_video_info(file_path)
            if error:
                self.window.logging_section.log_message(f"Warning: Could not read video metadata - {error}")
                duration_str = "Unknown"
            else:
                duration_str = format_duration(duration)
                self.window.logging_section.log_message(f"Video loaded: {duration_str} duration, {size_str}")
            
            
            self.window.details_section.update_details(file_name, duration_str, size_str, file_ext)
            self.window.details_section.set_placeholder_text("Local Video\nSelected")
            
            
            self.current_video_path = file_path
            self.current_video_duration = duration
            
            
            if duration > 0:
                max_duration = duration / 2
                max_offset = duration - 1.0  
                self.window.slicer_section.set_duration_range(max_duration)
                self.window.slicer_section.set_offset_range(max(0, max_offset))
                self.window.logging_section.log_message(f"Slicer configured: max cut duration {max_duration:.1f}s, max offset {max_offset:.1f}s")
            
            self.update_cut_button_state()
            
            
            if duration > 0:
                from moviepy import VideoFileClip
                try:
                    clip = VideoFileClip(file_path)
                    self.thumbnail_manager.extract_local_thumbnail(
                        clip, 
                        lambda thumb: self.window.details_section.set_thumbnail(thumb)
                    )
                    clip.close()
                except:
                    pass
            
        except Exception as e:
            self.window.logging_section.log_message(f"ERROR: Could not read video file - {e}")
    
    def on_duration_change(self, duration: float):
        """Handle duration slider changes"""
        if self.current_video_duration > 0:
            max_duration = self.current_video_duration / 2
            self.window.slicer_section.set_duration_range(max_duration)
    
    def on_offset_change(self, offset: float):
        """Handle offset slider changes"""
        
        if self.current_video_duration > 0:
            max_offset = self.current_video_duration - 1.0
            if offset > max_offset:
                self.window.slicer_section.set_offset_range(max(0, max_offset))
    
    def on_refresh_preview(self):
        """Handle preview refresh"""
        if not self.current_video_path:
            return
        
        duration = self.window.slicer_section.get_duration()
        offset = self.window.slicer_section.get_offset()
        
        def on_previews_ready(previews):
            self.window.slicer_section.display_previews(previews)
            self.window.slicer_section.reset_preview_button()
        
        def on_progress_update(progress):
            self.window.slicer_section.update_preview_progress(progress)
        
        self.thumbnail_manager.generate_preview_thumbnails(
            self.current_video_path, duration, offset, on_previews_ready,
            progress_callback=on_progress_update
        )
    
    def on_directory_chosen(self, directory: str):
        """Handle export directory selection"""
        self.update_cut_button_state()
    
    def on_cut_video(self):
        """Handle video cutting"""
        export_dir = self.window.slicer_section.get_export_directory()
        if not self.current_video_path or not export_dir:
            self.window.logging_section.log_message("ERROR: Please select a video and export directory.")
            return
        
        duration = self.window.slicer_section.get_duration()
        offset = self.window.slicer_section.get_offset()
        
        self.window.slicer_section.set_cut_button_text("Cutting...")
        self.window.slicer_section.update_cut_button_state(False)
        self.window.logging_section.reset_progress()
        
        def on_progress(progress_percent, message, current, total):
            self.window.logging_section.update_progress(progress_percent)
            self.window.logging_section.log_message(message)
        
        def on_completion(cuts_made, export_directory):
            self.window.logging_section.log_message(f"✓ Successfully created {cuts_made} image cuts!")
            self.window.logging_section.log_message(f"Files saved to: {export_directory}")
            self.window.slicer_section.set_cut_button_text("Cut")
            self.window.slicer_section.update_cut_button_state(True)
        
        def on_error(error):
            self.window.logging_section.log_message(f"ERROR: Failed to cut video - {error}")
            self.window.slicer_section.set_cut_button_text("Cut")
            self.window.slicer_section.update_cut_button_state(True)
        
        self.video_processor.cut_video_to_images(
            self.current_video_path, export_dir, duration, offset,
            on_progress, on_completion, on_error
        )
    
    def update_cut_button_state(self):
        """Update cut button state based on current conditions"""
        enabled = (self.current_video_path is not None and 
                  self.window.slicer_section.get_export_directory() is not None)
        self.window.slicer_section.update_cut_button_state(enabled)
    
    def run(self):
        """Start the application"""
        self.window.run()
