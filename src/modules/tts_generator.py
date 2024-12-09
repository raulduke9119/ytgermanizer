"""
Module for generating speech from text using either Tacotron2 or Bark TTS models.
"""
from pathlib import Path
import re
from typing import Optional, Literal, List, Tuple
import torch
from TTS.api import TTS
from scipy.io import wavfile
from bark import SAMPLE_RATE, generate_audio, preload_models
from pydub import AudioSegment
import numpy as np
from .file_manager import FileManager
from .cleanup import TempCleanup
import concurrent.futures
from tqdm import tqdm
import os

os.environ["SUNO_OFFLOAD_CPU"] = "False"     # CPU Offloading aktivieren
os.environ["SUNO_USE_SMALL_MODELS"] = "False" # Kleine Modelle verwenden

class TTSGenerator:
    def __init__(self, model_type: Literal["tacotron2", "bark"] = "tacotron2", use_gpu: bool = True):
        """
        Initialize TTS Generator with choice of model.
        
        Args:
            model_type (str): Type of TTS model to use ("tacotron2" or "bark")
            use_gpu (bool): Whether to use GPU acceleration
        """
        self.model_type = model_type
        self.use_gpu = use_gpu
        self.file_manager = FileManager()
        self.temp_cleanup = TempCleanup()
        
        if model_type == "tacotron2":
            self.model = TTS(
                model_name="tts_models/de/thorsten/tacotron2-DDC",
                progress_bar=True,
            )
            if use_gpu and torch.cuda.is_available():
                self.model.to('cuda')
        else:  # bark
            if use_gpu and not torch.cuda.is_available():
                print("Warning: GPU requested but not available. Using CPU instead.")
            # Download and load all models
            preload_models()
            self.speaker = "v2/de_speaker_6"  # German male voice

    def preprocess_text(self, text: str) -> str:
        """Preprocess text to ensure consistent formatting."""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Add period if text doesn't end with punctuation
        if text and not text[-1] in '.!?':
            text += '.'
        return text
    
    def split_text_into_chunks(self, text: str, max_chars: int = 150) -> list[str]:
        """Split text into chunks at sentence boundaries."""
        text = self.preprocess_text(text)
        
        # Split text into sentences
        sentences = re.split('([.!?]+)', text)
        
        chunks = []
        current_chunk = ""
        
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")
            
            # If current chunk is empty, add sentence regardless of length
            if not current_chunk:
                current_chunk = sentence
            # If adding the sentence doesn't exceed max_chars, add it
            elif len(current_chunk) + len(sentence) <= max_chars:
                current_chunk += sentence
            # Otherwise, store current chunk and start new one
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    def generate_speech_batch(self,
                            texts: List[str],
                            speaker: Optional[str] = None,
                            max_workers: int = 2) -> List[str]:
        """
        Generates speech for multiple texts in parallel using the selected model.
        
        Args:
            texts (List[str]): List of texts to convert to speech
            speaker (Optional[str]): Speaker preset (for Bark) or speaker ID (for Tacotron2)
            max_workers (int): Maximum number of parallel workers
            
        Returns:
            List[str]: List of paths to the generated audio files
        """
        # Preprocess all texts
        texts = [self.preprocess_text(text) for text in texts]
        
        if self.model_type != "tacotron2":
            # For Bark, process sequentially as it's more memory intensive
            return [self.generate_speech(text, speaker) for text in tqdm(texts)]
        
        output_paths = []
        
        def process_text(text: str) -> str:
            try:
                return self.generate_speech(text, speaker)
            except Exception as e:
                print(f"Error processing text: {text[:50]}... - {str(e)}")
                return None
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Process texts and collect results
            futures = [executor.submit(process_text, text) for text in texts]
            
            # Process completed futures as they complete
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(texts)):
                result = future.result()
                if result:
                    output_paths.append(result)
        
        return output_paths

    def generate_speech(self, 
                       text: str, 
                       speaker: Optional[str] = None) -> str:
        """
        Generates speech from text using the selected model.
        
        Args:
            text (str): Text to convert to speech
            speaker (Optional[str]): Speaker preset (for Bark) or speaker ID (for Tacotron2)
            
        Returns:
            str: Path to the generated audio file
        """
        try:
            # Preprocess text
            text = self.preprocess_text(text)
            
            # Generate unique output path
            output_path = str(self.file_manager.get_temp_path("tts_audio", ".wav"))
            
            if self.model_type == "tacotron2":
                # For Tacotron2, process the entire text at once
                self.model.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker=speaker
                )
            else:  # bark
                # Split text into chunks if using Bark
                text_chunks = self.split_text_into_chunks(text)
                print(f"Split text into {len(text_chunks)} chunks")
                
                # Generate audio for each chunk
                combined_audio = AudioSegment.empty()
                for i, chunk in enumerate(text_chunks, 1):
                    print(f"Generating audio for chunk {i}/{len(text_chunks)}")
                    audio_array = generate_audio(chunk, history_prompt=speaker or self.speaker)
                    
                    # Save chunk temporarily
                    chunk_path = str(self.file_manager.get_temp_path(f"chunk_{i}", ".wav"))
                    wavfile.write(chunk_path, SAMPLE_RATE, audio_array)
                    
                    # Add to combined audio
                    chunk_audio = AudioSegment.from_wav(chunk_path)
                    combined_audio += chunk_audio
                    
                    # Clean up chunk file
                    Path(chunk_path).unlink()
                
                # Export final combined audio
                combined_audio.export(output_path, format="wav")
            
            return output_path
            
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            raise
        finally:
            # Clean up old temporary files
            self.file_manager.cleanup_temp_files()

    def adjust_audio_speed(self, audio_path: str, target_duration: float) -> str:
        """
        Adjust the speed of the audio to match the target duration if needed.
        Only speeds up the audio, never slows it down.
        
        Args:
            audio_path (str): Path to the audio file
            target_duration (float): Target duration in seconds
            
        Returns:
            str: Path to the adjusted audio file (same as input if no adjustment needed)
        """
        # Load the audio
        audio = AudioSegment.from_wav(audio_path)
        current_duration = len(audio) / 1000.0  # Convert to seconds
        
        # If audio is shorter or equal to target, no need to adjust
        if current_duration <= target_duration:
            return audio_path
            
        # Calculate the required speed up factor
        # When we want to speed up, we need to reduce the frame rate
        # So we divide the frame rate by the speed factor
        speed_factor = current_duration / target_duration
        new_frame_rate = int(audio.frame_rate / speed_factor)
        
        # Create a new file path for the adjusted audio
        adjusted_path = str(self.file_manager.get_temp_path("adjusted_audio", ".wav"))
        
        # Speed up the audio by reducing the frame rate first, then setting it back
        adjusted_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": new_frame_rate
        }).set_frame_rate(audio.frame_rate)
        
        # Export the sped up audio
        adjusted_audio.export(adjusted_path, format="wav")
        
        # Verify the new duration
        new_audio = AudioSegment.from_wav(adjusted_path)
        new_duration = len(new_audio) / 1000.0
        print(f"Audio sped up: {current_duration:.2f}s -> {new_duration:.2f}s (target: {target_duration:.2f}s)")
        
        return adjusted_path

    def generate_speech_with_timing(self,
                                  text: str,
                                  target_duration: float,
                                  speaker: Optional[str] = None) -> Tuple[str, float]:
        """
        Generates speech from text and adjusts its speed to match target duration if needed.
        
        Args:
            text (str): Text to convert to speech
            target_duration (float): Target duration in seconds
            speaker (Optional[str]): Speaker preset (for Bark) or speaker ID (for Tacotron2)
            
        Returns:
            Tuple[str, float]: Tuple of (path to audio file, actual duration in seconds)
        """
        # First generate the speech normally
        audio_path = self.generate_speech(text, speaker)
        
        try:
            # Load the generated audio to get its duration
            audio = AudioSegment.from_wav(audio_path)
            current_duration = len(audio) / 1000.0  # Convert to seconds
            
            # If audio is longer than target duration, adjust its speed
            if current_duration > target_duration:
                print(f"Audio duration ({current_duration:.2f}s) exceeds target ({target_duration:.2f}s). Adjusting speed...")
                adjusted_path = self.adjust_audio_speed(audio_path, target_duration)
                
                # Get the new duration
                adjusted_audio = AudioSegment.from_wav(adjusted_path)
                actual_duration = len(adjusted_audio) / 1000.0
                
                # Clean up the original file if we created a new one
                if adjusted_path != audio_path:
                    Path(audio_path).unlink()
                
                return adjusted_path, actual_duration
            
            return audio_path, current_duration
            
        except Exception as e:
            print(f"Error adjusting audio speed: {str(e)}")
            return audio_path, current_duration

    def generate_speech_batch_with_timing(self,
                                        texts: List[str],
                                        target_durations: List[float],
                                        speaker: Optional[str] = None,
                                        max_workers: int = 2) -> List[Tuple[str, float]]:
        """
        Generates speech for multiple texts with timing constraints.
        
        Args:
            texts (List[str]): List of texts to convert to speech
            target_durations (List[float]): List of target durations in seconds
            speaker (Optional[str]): Speaker preset (for Bark) or speaker ID (for Tacotron2)
            max_workers (int): Maximum number of parallel workers
            
        Returns:
            List[Tuple[str, float]]: List of tuples (audio path, actual duration)
        """
        if len(texts) != len(target_durations):
            raise ValueError("Number of texts must match number of target durations")
            
        # Preprocess all texts
        texts = [self.preprocess_text(text) for text in texts]
        
        results = []
        
        def process_text_with_timing(text: str, target_duration: float) -> Optional[Tuple[str, float]]:
            try:
                return self.generate_speech_with_timing(text, target_duration, speaker)
            except Exception as e:
                print(f"Error processing text: {text[:50]}... - {str(e)}")
                return None
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create futures for all text-duration pairs
            futures = [
                executor.submit(process_text_with_timing, text, duration)
                for text, duration in zip(texts, target_durations)
            ]
            
            # Process completed futures as they complete
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(texts)):
                result = future.result()
                if result:
                    results.append(result)
        
        return results
