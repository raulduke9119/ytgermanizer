#!/usr/bin/env python3

"""
Main script for video translation and synchronization.
"""
import os
from pathlib import Path
from modules.video_downloader import download_video
from modules.audio_extractor import extract_audio
from modules.transcriber import transcribe_audio
from modules.translator import translate_text
from modules.tts_generator import TTSGenerator
from modules.synchronizer import Synchronizer
from modules.cleanup import TempCleanup

def ensure_downloads_dir():
    """Ensure downloads directory exists."""
    Path("downloads").mkdir(exist_ok=True)

def get_tts_model_choice() -> str:
    """Get user's choice of TTS model."""
    while True:
        print("\nSelect TTS model:")
        print("1. Tacotron2 (Thorsten German voice)")
        print("2. Bark (More expressive, slower)")
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            return "tacotron2"
        elif choice == "2":
            return "bark"
        else:
            print("Invalid choice. Please enter 1 or 2.")

def get_gpu_choice() -> bool:
    """Get user's choice for GPU usage."""
    while True:
        print("\nUse GPU for processing?")
        print("1. Yes (Recommended if available)")
        print("2. No (CPU only)")
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            return True
        elif choice == "2":
            return False
        else:
            print("Invalid choice. Please enter 1 or 2.")

def get_language_choice() -> str:
    """Get source language choice."""
    while True:
        print("\nSelect source video language:")
        print("1. English")
        print("2. Spanish")
        print("3. French")
        print("4. Italian")
        choice = input("Enter your choice (1-4): ").strip()
        
        language_codes = {
            "1": "en",
            "2": "es",
            "3": "fr",
            "4": "it"
        }
        
        if choice in language_codes:
            return language_codes[choice]
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def main():
    """Main function."""
    temp_cleanup = TempCleanup()
    try:
        # Check for AssemblyAI API key
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not api_key:
            raise ValueError(
                "AssemblyAI API key not found! Please set the ASSEMBLYAI_API_KEY environment variable."
            )
        
        # Print welcome message
        print("\n=== YouTube Video Translator ===")
        print("This tool will help you translate and dub your YouTube video to German.")
        
        # Ensure downloads directory exists
        ensure_downloads_dir()
        
        # Get input from user
        video_url = input("\nEnter YouTube video URL: ").strip()
        
        # Get language choice
        source_language = get_language_choice()
        
        # Get GPU choice
        use_gpu = get_gpu_choice()
        
        print("\nStarting video translation process...\n")
        
        with temp_cleanup:  # Use context manager for automatic cleanup
            # 1. Download video
            print("1. Downloading video...")
            video_path = download_video(video_url)
            print(f"Video downloaded to: {video_path}\n")
            
            # 2. Extract audio
            print("2. Extracting audio...")
            audio_path = extract_audio(video_path)
            print(f"Audio extracted to: {audio_path}\n")
            
            # 3. Transcribe audio
            print("\n3. Transcribing audio...")
            utterances = transcribe_audio(
                audio_path=audio_path,
                api_key=api_key,
                language_code=source_language
            )
            
            # Combine all utterances into a single text
            transcribed_text = " ".join(utterance.text for utterance in utterances)
            print("\nTranscription completed. Text:", transcribed_text[:200] + "..." if len(transcribed_text) > 200 else transcribed_text)
            
            # 4. Translate text
            print("4. Translating text to German...")
            translated_text = translate_text(transcribed_text)
            print("Translation completed\n")
            
            # 5. Get TTS model choice
            tts_model = get_tts_model_choice()
            
            # 6. Generate speech
            print("\n5. Generating German speech...")
            tts = TTSGenerator(model_type=tts_model, use_gpu=use_gpu)
            tts_audio_path = tts.generate_speech(translated_text)
            
            print("\n6. Synchronizing audio with video...")
            synchronizer = Synchronizer()
            final_video_path = synchronizer.sync_audio_with_video(
                video_path=video_path,
                audio_path=tts_audio_path
            )
            
            print(f"\nDone! Final video saved to: {final_video_path}")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        # Ensure cleanup happens even if there's an error
        temp_cleanup.cleanup()

if __name__ == "__main__":
    main()
