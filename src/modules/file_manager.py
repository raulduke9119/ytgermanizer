"""
Module for managing file operations and temporary files.
"""
import os
from pathlib import Path
import shutil
from datetime import datetime
import tempfile

class FileManager:
    def __init__(self, base_dir: str = "downloads"):
        """
        Initialize FileManager with base directory for all files.
        
        Args:
            base_dir (str): Base directory for all files
        """
        self.base_dir = Path(base_dir)
        self.temp_dir = self.base_dir / "temp"
        self.output_dir = self.base_dir / "output"
        self.init_directories()

    def init_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in [self.base_dir, self.temp_dir, self.output_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_temp_path(self, prefix: str, suffix: str) -> Path:
        """
        Get a temporary file path.
        
        Args:
            prefix (str): Prefix for the temp file
            suffix (str): File extension with dot
            
        Returns:
            Path: Path to temporary file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}{suffix}"
        return self.temp_dir / filename

    def get_output_path(self, prefix: str, suffix: str) -> Path:
        """
        Get an output file path.
        
        Args:
            prefix (str): Prefix for the output file
            suffix (str): File extension with dot
            
        Returns:
            Path: Path to output file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}{suffix}"
        return self.output_dir / filename

    def cleanup_temp_files(self, max_age_hours: int = 24):
        """
        Clean up temporary files older than specified hours.
        
        Args:
            max_age_hours (int): Maximum age of temp files in hours
        """
        current_time = datetime.now().timestamp()
        
        for file_path in self.temp_dir.glob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_hours * 3600:
                    try:
                        file_path.unlink()
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {str(e)}")

    def cleanup_old_outputs(self, max_files: int = 10):
        """
        Keep only the most recent output files.
        
        Args:
            max_files (int): Maximum number of output files to keep
        """
        files = list(self.output_dir.glob("*"))
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for file_path in files[max_files:]:
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Failed to delete {file_path}: {str(e)}")

    def save_output(self, source_path: Path, prefix: str) -> Path:
        """
        Save a file to the output directory with proper naming.
        
        Args:
            source_path (Path): Source file path
            prefix (str): Prefix for the output file
            
        Returns:
            Path: Path to saved output file
        """
        output_path = self.get_output_path(prefix, source_path.suffix)
        shutil.copy2(source_path, output_path)
        return output_path
