"""
Module for extracting audio from video files using ffmpeg.
"""
from pathlib import Path
import ffmpeg
import subprocess

def extract_audio(video_path: str, audio_output: str = "downloads/audio.wav") -> str:
    """
    Extracts audio from a video file using ffmpeg.
    
    Args:
        video_path (str): Path to the input video file
        audio_output (str): Path where the audio will be saved
        
    Returns:
        str: Path to the extracted audio file
    """
    # Ensure the output directory exists
    Path(audio_output).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Construct ffmpeg command
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vn',  # No video
            '-acodec', 'pcm_s16le',  # PCM 16-bit format
            '-ar', '44100',  # 44.1kHz sampling rate
            '-ac', '1',  # Mono audio
            '-y',  # Overwrite output
            audio_output
        ]
        
        # Run ffmpeg command
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        
        # Verify the output file exists and has size > 0
        output_file = Path(audio_output)
        if not output_file.exists() or output_file.stat().st_size == 0:
            raise Exception("Audio extraction failed: Output file is empty or doesn't exist")
            
        return audio_output
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to extract audio: {e.stderr.decode()}")
    except Exception as e:
        raise Exception(f"An error occurred while extracting audio: {str(e)}")
