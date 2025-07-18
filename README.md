

A modern YouTube video downloader and frame extractor with a sleek GUI.



- Download YouTube videos (video-only format)
- Extract frames from videos at specified intervals
- Preview thumbnails before extraction
- Real-time progress tracking and logging
- Modern dark theme UI



1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```



1. **Download YouTube Video**: Paste a YouTube URL and click Download
2. **Load Local Video**: Use Browse to select a local video file
3. **Configure Slicer**: Set the cut duration using the slider
4. **Preview**: Click "Refresh Preview" to see thumbnail previews
5. **Extract Frames**: Choose export directory and click Cut



```
SMV-Extracter/
├── main.py              
├── src/
│   ├── __init__.py
│   ├── app.py           
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py    
│   │   ├── input_section.py  
│   │   ├── details_section.py 
│   │   ├── logging_section.py 
│   │   └── slicer_section.py  
│   ├── core/
│   │   ├── __init__.py
│   │   ├── downloader.py     
│   │   ├── video_processor.py 
│   │   └── thumbnail_manager.py 
│   └── utils/
│       ├── __init__.py
│       ├── logger.py         
│       └── helpers.py        
├── requirements.txt
└── README.md
```



- Python 3.7+
- tkinter (usually included with Python)
- yt-dlp
- sv-ttk
- requests
- Pillow
- moviepy
