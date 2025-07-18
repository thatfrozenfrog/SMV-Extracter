"""
Video processing and frame extraction functionality
"""
import os
import threading
from typing import Callable
from PIL import Image
from moviepy import VideoFileClip
from ..utils.helpers import create_progress_bar


class VideoProcessor:
    """Handles video processing operations"""
    
    def __init__(self):
        pass
    
    def get_video_info(self, file_path: str) -> tuple:
        """Get video information using moviepy"""
        try:
            clip = VideoFileClip(file_path)
            duration = clip.duration
            clip.close()
            return duration, None
        except Exception as e:
            return 0, str(e)
    
    def cut_video_to_images(self, video_path: str, export_directory: str, duration: float, offset: float,
                           progress_callback: Callable[[float, str, int, int], None],
                           completion_callback: Callable[[int, str], None],
                           error_callback: Callable[[str], None]):
        """Cut video into segments and save as images with offset"""
        def do_cut():
            try:
                clip = VideoFileClip(video_path)
                video_name = os.path.splitext(os.path.basename(video_path))[0]
                
                
                available_duration = clip.duration - offset
                if available_duration <= 0:
                    error_callback("Offset is beyond video duration")
                    return
                
                total_cuts = int(available_duration / duration)
                progress_callback(0, f"Starting to cut video into {total_cuts} segments from offset {offset:.1f}s...", 0, total_cuts)
                
                cuts_made = 0
                for i in range(total_cuts):
                    timestamp = offset + (i * duration)
                    if timestamp >= clip.duration:
                        break
                        
                    frame = clip.get_frame(timestamp)
                    img = Image.fromarray(frame)
                    
                    
                    filename = f"{video_name}_cut_{i+1:03d}_offset_{offset:.1f}s_at_{timestamp:.1f}s.jpg"
                    filepath = os.path.join(export_directory, filename)
                    img.save(filepath, "JPEG", quality=95)
                    cuts_made += 1
                    
                    
                    progress_percent = (cuts_made / total_cuts) * 100
                    progress_bar = create_progress_bar(progress_percent)
                    progress_message = f"[{progress_bar}] {progress_percent:.1f}% - Cut {cuts_made}/{total_cuts} saved"
                    progress_callback(progress_percent, progress_message, cuts_made, total_cuts)
                
                clip.close()
                completion_callback(cuts_made, export_directory)
                
            except Exception as e:
                error_callback(str(e))
        
        threading.Thread(target=do_cut, daemon=True).start()
