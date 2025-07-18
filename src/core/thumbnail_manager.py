"""
Thumbnail management utilities
"""
import io
import threading
from typing import Optional, Callable
import requests
from PIL import Image, ImageTk
from moviepy import VideoFileClip


class ThumbnailManager:
    """Manages thumbnail generation and display"""
    
    def __init__(self):
        self.current_thumbnail = None
    
    def extract_local_thumbnail(self, clip: VideoFileClip, callback: Callable[[ImageTk.PhotoImage], None]):
        """Extract thumbnail from local video file"""
        try:
            
            frame_time = min(clip.duration * 0.1, 5.0) if clip.duration > 5 else clip.duration / 2
            frame = clip.get_frame(frame_time)
            
            
            img = Image.fromarray(frame)
            img = img.resize((120, 90), Image.Resampling.LANCZOS)
            
            
            thumbnail = ImageTk.PhotoImage(img)
            self.current_thumbnail = thumbnail
            callback(thumbnail)
            
        except Exception:
            callback(None)
    
    def download_youtube_thumbnail(self, thumbnail_url: str, 
                                 success_callback: Callable[[ImageTk.PhotoImage], None],
                                 error_callback: Callable[[], None]):
        """Download and display YouTube thumbnail"""
        def fetch_thumbnail():
            try:
                response = requests.get(thumbnail_url, timeout=10)
                response.raise_for_status()
                
                
                img = Image.open(io.BytesIO(response.content))
                img = img.resize((120, 90), Image.Resampling.LANCZOS)
                
                
                thumbnail = ImageTk.PhotoImage(img)
                self.current_thumbnail = thumbnail
                success_callback(thumbnail)
                
            except Exception:
                error_callback()
        
        threading.Thread(target=fetch_thumbnail, daemon=True).start()
    
    def generate_preview_thumbnails(self, video_path: str, duration: float, offset: float,
                                  callback: Callable[[list], None], max_previews: int = 6,
                                  progress_callback: Optional[Callable[[float], None]] = None):
        """Generate preview thumbnails for video cutting with offset"""
        def generate_preview():
            try:
                clip = VideoFileClip(video_path)
                previews = []
                
                
                segment_start = offset
                segment_end = min(offset + (duration * max_previews), clip.duration)
                
                
                if segment_end > segment_start:
                    subclip = clip.subclipped(segment_start, segment_end)
                    
                    
                    if progress_callback:
                        progress_callback(0.0)
                    
                    for i in range(max_previews):
                        timestamp = offset + (i * duration)
                        if timestamp >= clip.duration:
                            break
                        
                        
                        subclip_time = timestamp - segment_start
                        if subclip_time >= subclip.duration:
                            break
                            
                        frame = subclip.get_frame(subclip_time)
                        img = Image.fromarray(frame)
                        img = img.resize((80, 60), Image.Resampling.LANCZOS)
                        
                        
                        from PIL import ImageDraw, ImageFont
                        draw = ImageDraw.Draw(img)
                        timestamp_text = f"{timestamp:.1f}s"
                        
                        try:
                            font = ImageFont.truetype("arial.ttf", 10)
                        except:
                            font = ImageFont.load_default()
                        
                        draw.text((2, 2), timestamp_text, fill="white", font=font)
                        draw.text((1, 1), timestamp_text, fill="black", font=font)
                        
                        thumbnail = ImageTk.PhotoImage(img)
                        previews.append((thumbnail, timestamp))
                        
                        
                        if progress_callback:
                            progress = ((i + 1) / max_previews) * 100.0
                            progress_callback(progress)
                    
                    subclip.close()
                
                clip.close()
                
                if progress_callback:
                    progress_callback(100.0)
                callback(previews)
                
            except Exception as e:
                print(f"Preview generation error: {e}")
                
                if progress_callback:
                    progress_callback(100.0)
                callback([])
        
        threading.Thread(target=generate_preview, daemon=True).start()
