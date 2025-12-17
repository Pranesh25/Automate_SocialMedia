"""Media file handling utilities"""

import os
from typing import List, Optional, Tuple
from pathlib import Path
import logging

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class MediaHandler:
    """Handle media files (images, videos) for social media posting"""

    # Supported file extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv'}

    def __init__(self, media_folder: str = "./media"):
        """
        Initialize media handler
        
        Args:
            media_folder: Path to folder containing media files
        """
        self.media_folder = Path(media_folder)
        self.logger = logging.getLogger(__name__)

        # Create media folder if it doesn't exist
        self.media_folder.mkdir(parents=True, exist_ok=True)

    def is_image(self, file_path: str) -> bool:
        """
        Check if file is an image
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is an image, False otherwise
        """
        return Path(file_path).suffix.lower() in self.IMAGE_EXTENSIONS

    def is_video(self, file_path: str) -> bool:
        """
        Check if file is a video
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is a video, False otherwise
        """
        return Path(file_path).suffix.lower() in self.VIDEO_EXTENSIONS

    def validate_file(self, file_path: str) -> bool:
        """
        Validate that a file exists and is accessible
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file exists and is accessible, False otherwise
        """
        path = Path(file_path)
        if not path.exists():
            self.logger.error(f"File does not exist: {file_path}")
            return False
        if not path.is_file():
            self.logger.error(f"Path is not a file: {file_path}")
            return False
        return True

    def get_image_dimensions(self, image_path: str) -> Optional[Tuple[int, int]]:
        """
        Get dimensions of an image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (width, height) or None if unable to get dimensions
        """
        if not HAS_PIL:
            self.logger.warning("PIL not available, cannot get image dimensions")
            return None

        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception as e:
            self.logger.error(f"Error getting image dimensions: {e}")
            return None

    def resize_image(
        self,
        image_path: str,
        max_width: int,
        max_height: int,
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Resize an image while maintaining aspect ratio
        
        Args:
            image_path: Path to the input image
            max_width: Maximum width
            max_height: Maximum height
            output_path: Path for output image (generates if None)
            
        Returns:
            Path to resized image or None if failed
        """
        if not HAS_PIL:
            self.logger.warning("PIL not available, cannot resize image")
            return None

        try:
            with Image.open(image_path) as img:
                # Use appropriate resampling filter based on Pillow version
                try:
                    # Pillow >= 10.0.0
                    resample_filter = Image.Resampling.LANCZOS
                except AttributeError:
                    # Pillow < 10.0.0
                    resample_filter = Image.LANCZOS
                
                img.thumbnail((max_width, max_height), resample_filter)
                
                if output_path is None:
                    path = Path(image_path)
                    output_path = str(self.media_folder / f"{path.stem}_resized{path.suffix}")
                
                img.save(output_path)
                self.logger.info(f"Resized image saved to: {output_path}")
                return output_path
        except Exception as e:
            self.logger.error(f"Error resizing image: {e}")
            return None

    def get_file_size_mb(self, file_path: str) -> float:
        """
        Get file size in megabytes
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in MB
        """
        return os.path.getsize(file_path) / (1024 * 1024)

    def list_media_files(self, media_type: Optional[str] = None) -> List[str]:
        """
        List all media files in the media folder
        
        Args:
            media_type: Filter by 'image' or 'video', or None for all
            
        Returns:
            List of file paths
        """
        files = []
        for file_path in self.media_folder.iterdir():
            if file_path.is_file():
                if media_type == 'image' and self.is_image(str(file_path)):
                    files.append(str(file_path))
                elif media_type == 'video' and self.is_video(str(file_path)):
                    files.append(str(file_path))
                elif media_type is None and (self.is_image(str(file_path)) or self.is_video(str(file_path))):
                    files.append(str(file_path))
        return sorted(files)
