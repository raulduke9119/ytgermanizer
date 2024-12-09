"""
Module for adjusting speed of video and audio files to match durations.
"""
from pathlib import Path
from typing import Tuple, Optional
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import numpy as np
from .cleanup import TempCleanup

class MediaSpeedAdjuster:
    def __init__(self):
        """Initialize the MediaSpeedAdjuster."""
        self.temp_cleanup = TempCleanup()

    def get_video_duration(self, video_path: str) -> float:
        """Get the duration of a video file in seconds."""
        with VideoFileClip(video_path) as video:
            return video.duration

    def get_audio_duration(self, audio_path: str) -> float:
        """Get the duration of an audio file in seconds."""
        audio = AudioSegment.from_wav(audio_path)
        return len(audio) / 1000.0

    def adjust_video_speed(self, 
                         video_path: str, 
                         target_duration: float,
                         preserve_pitch: bool = True) -> str:
        """
        Adjust video speed to match target duration.
        
        Args:
            video_path (str): Path to the video file
            target_duration (float): Target duration in seconds
            preserve_pitch (bool): Whether to preserve audio pitch when adjusting speed
            
        Returns:
            str: Path to the adjusted video file
        """
        try:
            # Load the video
            video = VideoFileClip(video_path)
            current_duration = video.duration
            
            # Calculate the speed factor
            speed_factor = current_duration / target_duration
            
            # Create adjusted video
            adjusted_video = video.speedx(factor=speed_factor)
            
            # Create output path in temp directory
            output_filename = f"adjusted_{Path(video_path).name}"
            output_path = str(self.temp_cleanup.get_temp_path(output_filename))
            
            # Write the adjusted video
            adjusted_video.write_videofile(
                output_path, 
                codec='libx264',
                audio=False,  # Don't include audio
                preset='medium',
                fps=video.fps
            )
            
            # Clean up
            video.close()
            adjusted_video.close()
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Failed to adjust video speed: {str(e)}")

    def adjust_audio_speed(self, 
                         audio_path: str, 
                         target_duration: float,
                         preserve_pitch: bool = True) -> str:
        """
        Adjust audio speed to match target duration.
        
        Args:
            audio_path (str): Path to the audio file
            target_duration (float): Target duration in seconds
            preserve_pitch (bool): Whether to preserve pitch when adjusting speed
            
        Returns:
            str: Path to the adjusted audio file
        """
        try:
            # Load the audio
            audio = AudioSegment.from_wav(audio_path)
            current_duration = len(audio) / 1000.0  # Convert to seconds
            
            # Calculate the speed factor
            speed_factor = current_duration / target_duration
            
            if preserve_pitch:
                # Use frame rate adjustment for pitch-preserved speed change
                new_frame_rate = int(audio.frame_rate * speed_factor)
                adjusted_audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": new_frame_rate
                }).set_frame_rate(audio.frame_rate)
            else:
                # Simple resampling for non-pitch-preserved speed change
                samples = np.array(audio.get_array_of_samples())
                adjusted_samples = np.interp(
                    np.linspace(0, len(samples), int(len(samples) / speed_factor)),
                    np.arange(len(samples)),
                    samples
                ).astype(np.int16)
                adjusted_audio = audio._spawn(adjusted_samples.tobytes())
            
            # Create output path in temp directory
            output_filename = f"adjusted_{Path(audio_path).name}"
            output_path = str(self.temp_cleanup.get_temp_path(output_filename))
            
            # Export the adjusted audio
            adjusted_audio.export(output_path, format="wav")
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Failed to adjust audio speed: {str(e)}")

    def harmonize_durations(self, 
                          video_path: str, 
                          audio_path: str,
                          target_duration: Optional[float] = None,
                          max_adjustment_ratio: float = 1.5,
                          preserve_pitch: bool = True) -> Tuple[str, str]:
        """
        Adjust video and audio speeds to meet at a target duration.
        
        Args:
            video_path (str): Path to the video file
            audio_path (str): Path to the audio file
            target_duration (Optional[float]): Target duration in seconds. If None, uses the average duration
            max_adjustment_ratio (float): Maximum allowed speed change ratio
            preserve_pitch (bool): Whether to preserve pitch when adjusting speed
            
        Returns:
            Tuple[str, str]: Paths to the adjusted (video, audio) files
        """
        try:
            # Get current durations
            video_duration = self.get_video_duration(video_path)
            audio_duration = self.get_audio_duration(audio_path)
            
            # Calculate target duration if not provided
            if target_duration is None:
                target_duration = (video_duration + audio_duration) / 2
            
            print(f"Original durations - Video: {video_duration:.2f}s, Audio: {audio_duration:.2f}s")
            print(f"Target duration: {target_duration:.2f}s")
            
            # Check if adjustment is within acceptable range
            video_ratio = max(video_duration / target_duration, target_duration / video_duration)
            audio_ratio = max(audio_duration / target_duration, target_duration / audio_duration)
            
            if max(video_ratio, audio_ratio) > max_adjustment_ratio:
                raise ValueError(
                    f"Required speed adjustment ({max(video_ratio, audio_ratio):.2f}x) "
                    f"exceeds maximum allowed ratio ({max_adjustment_ratio}x)"
                )
            
            # Adjust both video and audio to the target duration
            adjusted_video_path = self.adjust_video_speed(
                video_path, 
                target_duration,
                preserve_pitch=preserve_pitch
            )
            
            adjusted_audio_path = self.adjust_audio_speed(
                audio_path, 
                target_duration,
                preserve_pitch=preserve_pitch
            )
            
            # Verify final durations
            final_video_duration = self.get_video_duration(adjusted_video_path)
            final_audio_duration = self.get_audio_duration(adjusted_audio_path)
            
            print(f"Final durations - Video: {final_video_duration:.2f}s, Audio: {final_audio_duration:.2f}s")
            
            return adjusted_video_path, adjusted_audio_path
            
        except Exception as e:
            raise RuntimeError(f"Failed to harmonize durations: {str(e)}")
