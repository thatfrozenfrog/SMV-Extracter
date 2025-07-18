"""
YouTube video downloader functionality
"""
import threading
import yt_dlp
from typing import Callable, Optional
from ..utils.logger import YTDLPLogger


class YouTubeDownloader:
    """Handles YouTube video downloading operations"""
    
    def __init__(self):
        self.download_thread: Optional[threading.Thread] = None
        self.download_cancelled = False
    
    def get_video_info(self, url: str, callback: Callable[[dict], None], 
                      error_callback: Callable[[str], None]):
        """Get YouTube video information without downloading"""
        def fetch_info():
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if info:
                        callback(info)
            except Exception as e:
                error_callback(str(e))
        
        threading.Thread(target=fetch_info, daemon=True).start()
    
    def download_video(self, url: str, 
                      progress_callback: Callable[[dict], None],
                      completion_callback: Callable[[str], None],
                      error_callback: Callable[[str], None],
                      log_callback: Callable[[str], None]):
        """Download YouTube video"""
        def do_download():
            self.download_cancelled = False
            
            def progress_hook(d):
                if self.download_cancelled:
                    raise Exception("Download cancelled by user")
                progress_callback(d)
                
            log_callback("Starting download...")
            
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'bestvideo[ext=mp4]+none/bestvideo[ext=mp4]',
                'merge_output_format': 'mp4',
                'progress_hooks': [progress_hook],
                'logger': YTDLPLogger(log_callback),
                'verbose': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
                if not self.download_cancelled:
                    log_callback("✓ Video-only download completed successfully!")
                    
            except Exception as e:
                if not self.download_cancelled:
                    error_callback(f"Failed to download - {e}")
                elif "cancelled by user" in str(e):
                    log_callback("Download cancelled by user")
        
        self.download_thread = threading.Thread(target=do_download, daemon=True)
        self.download_thread.start()
    
    def cancel_download(self):
        """Cancel the current download"""
        self.download_cancelled = True
