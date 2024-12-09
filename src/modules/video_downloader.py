"""
Module for downloading YouTube videos using yt-dlp.
"""
from pathlib import Path
from yt_dlp import YoutubeDL

def download_video(url: str, output_path: str = "downloads/video.mp4") -> str:
    """
    Downloads a YouTube video and saves it to the specified path.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Path where the video will be saved
        
    Returns:
        str: Path to the downloaded video file
    """
    # Ensure the output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'format': 'best',  # Download best quality
        'outtmpl': output_path,
        'quiet': False,  # Show progress
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")
