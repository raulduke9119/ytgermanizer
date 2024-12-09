"""
Module for transcribing audio using AssemblyAI API with speaker diarization support.
"""
import time
import requests
import os
import subprocess
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from .file_manager import FileManager

@dataclass
class Utterance:
    """Represents a single utterance in the transcription."""
    speaker: str
    text: str
    start: int  # milliseconds
    end: int    # milliseconds
    confidence: float
    words: List[Dict[str, Any]]

class TranscriptionError(Exception):
    """Custom exception for transcription-related errors."""
    pass

def convert_audio_to_mp3(input_path: str, file_manager: FileManager) -> str:
    """
    Convert audio file to MP3 format for better compatibility.
    
    Args:
        input_path (str): Path to input audio file
        file_manager (FileManager): File manager instance
        
    Returns:
        str: Path to converted MP3 file
    """
    output_path = str(file_manager.get_temp_path("converted_audio", ".mp3"))
    try:
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-acodec', 'libmp3lame',
            '-ac', '1',  # mono (required for speaker diarization)
            '-ar', '44100',  # 44.1kHz
            '-y',  # overwrite output
            output_path
        ]
        
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if process.returncode != 0:
            raise TranscriptionError(f"FFmpeg conversion failed: {process.stderr.decode()}")
            
        return output_path
        
    except Exception as e:
        raise TranscriptionError(f"Failed to convert audio to MP3: {str(e)}")

def upload_audio(audio_path: str, api_key: str) -> str:
    """
    Uploads an audio file to AssemblyAI.
    
    Args:
        audio_path (str): Path to the audio file
        api_key (str): AssemblyAI API key
        
    Returns:
        str: Upload URL for the audio file
    """
    try:
        print(f"Uploading audio file: {audio_path} (size: {os.path.getsize(audio_path)} bytes)")
        
        def read_file(file_path):
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(5242880)  # Read in 5MB chunks
                    if not data:
                        break
                    yield data
                    
        headers = {
            'authorization': api_key,
            'content-type': 'application/json'
        }
        
        upload_response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers={'authorization': api_key},
            data=read_file(audio_path)
        )
        
        if upload_response.status_code == 200:
            print(f"Successfully uploaded audio to: {upload_response.json()['upload_url']}")
            return upload_response.json()['upload_url']
        else:
            raise TranscriptionError(f"Upload failed: {upload_response.text}")
            
    except Exception as e:
        raise TranscriptionError(f"Failed to upload audio: {str(e)}")

def transcribe_audio(
    audio_path: str,
    api_key: str,
    language_code: str = "en",
    speakers_expected: Optional[int] = None
) -> List[Utterance]:
    """
    Transcribes audio using AssemblyAI API with speaker diarization.
    
    Args:
        audio_path (str): Path to the audio file
        api_key (str): AssemblyAI API key
        language_code (str): Language code for transcription (default: "en")
        speakers_expected (Optional[int]): Expected number of speakers (improves accuracy)
        
    Returns:
        List[Utterance]: List of transcribed utterances with speaker information
    """
    try:
        file_manager = FileManager()
        
        # Convert audio to MP3 if needed
        if not audio_path.lower().endswith('.mp3'):
            print("Converting audio to MP3 format...")
            audio_path = convert_audio_to_mp3(audio_path, file_manager)
        
        print("Uploading audio file...")
        upload_url = upload_audio(audio_path, api_key)
        
        headers = {
            "authorization": api_key,
            "content-type": "application/json"
        }
        
        # Configure transcription options
        data = {
            "audio_url": upload_url,
            "language_code": language_code,
            "speaker_labels": True
        }
        if speakers_expected:
            data["speakers_expected"] = speakers_expected
            
        # Start transcription
        response = requests.post("https://api.assemblyai.com/v2/transcript", json=data, headers=headers)
        if response.status_code != 200:
            raise TranscriptionError(f"Failed to start transcription: {response.text}")
            
        transcript_id = response.json()['id']
        polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        
        print("Processing audio... This may take a few minutes.")
        while True:
            transcription = requests.get(polling_endpoint, headers=headers).json()
            
            if transcription['status'] == 'completed':
                utterances = []
                # Check if 'utterances' exists and is not empty
                if 'utterances' in transcription and transcription['utterances']:
                    for utterance in transcription['utterances']:
                        utterances.append(Utterance(
                            speaker=utterance['speaker'],
                            text=utterance['text'],
                            start=utterance['start'],
                            end=utterance['end'],
                            confidence=utterance.get('confidence', 0.0),
                            words=utterance.get('words', [])
                        ))
                else:
                    # If no utterances, create a single utterance from the full text
                    utterances.append(Utterance(
                        speaker="speaker_1",
                        text=transcription['text'],
                        start=0,
                        end=int(float(transcription['audio_duration']) * 1000),
                        confidence=1.0,
                        words=[]
                    ))
                return utterances
                
            elif transcription['status'] == 'error':
                raise TranscriptionError(f"Transcription failed: {transcription['error']}")
                
            print(".", end="", flush=True)  # Show progress
            time.sleep(3)
            
    except Exception as e:
        raise TranscriptionError(f"Transcription failed: {str(e)}")
    finally:
        # Clean up temporary files
        if 'file_manager' in locals():
            file_manager.cleanup_temp_files()
