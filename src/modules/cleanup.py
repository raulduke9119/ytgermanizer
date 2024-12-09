"""
Module for managing temporary file cleanup.
"""
import os
import shutil
from pathlib import Path
import logging
from typing import Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TempCleanup:
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize the temp cleanup handler.
        
        Args:
            base_dir (Optional[str]): Base directory for temp files. If None, uses the default temp directory
        """
        if base_dir:
            self.temp_dir = Path(base_dir).absolute()
        else:
            # Get the project root directory (src's parent)
            project_root = Path(__file__).parent.parent.parent
            self.downloads_dir = project_root / "downloads"
            self.temp_dir = self.downloads_dir / "temp"
        
    def ensure_temp_dir(self) -> Path:
        """Create temp directory if it doesn't exist and return its path."""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        return self.temp_dir
        
    def cleanup_specific_files(self):
        """Clean up specific files in the downloads directory."""
        specific_files = [
            "audio.wav",
            "video.mp4"
        ]
        
        try:
            if self.downloads_dir.exists():
                for filename in specific_files:
                    file_path = self.downloads_dir / filename
                    if file_path.exists():
                        try:
                            file_path.unlink()
                            logger.info(f"Deleted file: {file_path}")
                        except Exception as e:
                            logger.error(f"Error while deleting {file_path}: {str(e)}")
        except Exception as e:
            logger.error(f"Error during specific file cleanup: {str(e)}")
        
    def cleanup(self, pattern: Optional[str] = None):
        """Remove files in the temp directory and specific files in downloads.
        
        Args:
            pattern (Optional[str]): If provided, only delete files matching this pattern in temp dir
        """
        # First clean up the temp directory
        try:
            if self.temp_dir.exists():
                for item in self.temp_dir.iterdir():
                    try:
                        if pattern and not str(item).endswith(pattern):
                            continue
                            
                        if item.is_file():
                            item.unlink()
                            logger.info(f"Deleted temporary file: {item}")
                        elif item.is_dir():
                            shutil.rmtree(item)
                            logger.info(f"Deleted temporary directory: {item}")
                    except Exception as e:
                        logger.error(f"Error while deleting {item}: {str(e)}")
                logger.info("Temporary files cleanup completed")
            else:
                logger.warning(f"Temp directory {self.temp_dir} does not exist")
        except Exception as e:
            logger.error(f"Error during temp directory cleanup: {str(e)}")
            
        # Then clean up specific files
        self.cleanup_specific_files()
            
    def get_temp_path(self, filename: str) -> Path:
        """Get a path for a temporary file.
        
        Args:
            filename (str): Name of the temporary file
            
        Returns:
            Path: Full path to the temporary file
        """
        return self.ensure_temp_dir() / filename
            
    def __enter__(self):
        """Context manager entry point."""
        self.ensure_temp_dir()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point - ensures cleanup is performed."""
        self.cleanup()
