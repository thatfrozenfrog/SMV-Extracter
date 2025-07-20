"""
SMV Extractor - YouTube video downloader and frame extractor
Entry point for the application
"""

if __name__ == "__main__":
    import sys
    
    
    if getattr(sys, 'frozen', False):
        print("Starting SMV-Extracter...")
        print("Please wait while the application loads...")
    
    from src.app import SMVExtractorApp
    
    app = SMVExtractorApp()
    app.run()
