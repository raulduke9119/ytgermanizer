"""
Module for synchronizing audio with video using moviepy.
"""
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from .file_manager import FileManager
from .media_speed_adjuster import MediaSpeedAdjuster

class Synchronizer:
    def __init__(self):
        """Initialize Synchronizer with FileManager."""
        self.file_manager = FileManager()
        self.speed_adjuster = MediaSpeedAdjuster()

    def sync_audio_with_video(
        self,
        video_path: str,
        audio_path: str,
        preserve_pitch: bool = True,
        max_speed_change: float = 1.5
    ) -> str:
        """
        Synchronizes TTS audio with video by adjusting speeds to match durations.
        
        Args:
            video_path (str): Path to the input video file
            audio_path (str): Path to the TTS audio file
            preserve_pitch (bool): Whether to preserve pitch when adjusting speed
            max_speed_change (float): Maximum allowed speed change ratio
            
        Returns:
            str: Path to the synchronized video file
        """
        try:
            print("Loading and analyzing media files...")
            video_duration = self.speed_adjuster.get_video_duration(video_path)
            audio_duration = self.speed_adjuster.get_audio_duration(audio_path)
            
            print(f"Original video duration: {video_duration:.2f}s")
            print(f"Original audio duration: {audio_duration:.2f}s")
            
            # Calculate target duration (use audio duration as target)
            target_duration = audio_duration
            
            # Adjust video and audio speeds
            adjusted_video_path, adjusted_audio_path = self.speed_adjuster.harmonize_durations(
                video_path=video_path,
                audio_path=audio_path,
                target_duration=target_duration,
                max_adjustment_ratio=max_speed_change,
                preserve_pitch=preserve_pitch
            )
            
            # Load adjusted files
            video = VideoFileClip(adjusted_video_path)
            audio = AudioFileClip(adjusted_audio_path)
            
            # Create final video with synchronized audio
            final_video = video.set_audio(audio)
            
            # Save to output directory with specific codec settings
            output_path = self.file_manager.get_output_path("synchronized_video", ".mp4")
            print(f"Saving synchronized video to {output_path}...")
            
            final_video.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=str(self.file_manager.get_temp_path("temp_audio", ".m4a")),
                remove_temp=True,
                fps=video.fps
            )
            
            # Clean up
            video.close()
            audio.close()
            final_video.close()
            
            return str(output_path)
            
        except Exception as e:
            print(f"Error: Failed to synchronize audio with video: {str(e)}")
            raise

    def create_video_with_subtitles(
        self,
        video_path: str,
        subtitles: list,
    ) -> str:
        """
        Creates a video with synchronized subtitles.
        
        Args:
            video_path (str): Path to the input video file
            subtitles (list): List of subtitle dictionaries with text and timing
            
        Returns:
            str: Path to the final video with subtitles
        """
        # TODO: Implement subtitle synchronization
        pass
