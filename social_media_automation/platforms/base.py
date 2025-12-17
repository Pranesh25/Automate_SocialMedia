"""Base class for all social media platform posters"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import logging


class SocialMediaPoster(ABC):
    """Abstract base class for social media posting"""

    def __init__(self, platform_name: str):
        """
        Initialize the social media poster
        
        Args:
            platform_name: Name of the social media platform
        """
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"{__name__}.{platform_name}")
        self.authenticated = False

    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the social media platform
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        pass

    @abstractmethod
    def post_text(self, text: str) -> Dict[str, Any]:
        """
        Post text-only content
        
        Args:
            text: Text content to post
            
        Returns:
            Dict containing post information (id, url, etc.)
        """
        pass

    @abstractmethod
    def post_image(self, text: str, image_path: str) -> Dict[str, Any]:
        """
        Post text with image
        
        Args:
            text: Text content to post
            image_path: Path to the image file
            
        Returns:
            Dict containing post information (id, url, etc.)
        """
        pass

    @abstractmethod
    def post_video(self, text: str, video_path: str) -> Dict[str, Any]:
        """
        Post text with video
        
        Args:
            text: Text content to post
            video_path: Path to the video file
            
        Returns:
            Dict containing post information (id, url, etc.)
        """
        pass

    def post_multiple_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """
        Post text with multiple images
        
        Args:
            text: Text content to post
            image_paths: List of paths to image files
            
        Returns:
            Dict containing post information (id, url, etc.)
        """
        # Default implementation - can be overridden by platforms that support it
        self.logger.warning(f"{self.platform_name} may not support multiple images natively")
        if image_paths:
            return self.post_image(text, image_paths[0])
        return self.post_text(text)

    def validate_credentials(self) -> bool:
        """
        Validate that required credentials are present
        
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        return self.authenticated

    def get_platform_name(self) -> str:
        """Get the platform name"""
        return self.platform_name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(platform='{self.platform_name}', authenticated={self.authenticated})>"
