"""Central manager for social media automation"""

from typing import List, Dict, Any, Optional
import logging
from .platforms.twitter_poster import TwitterPoster
from .platforms.facebook_poster import FacebookPoster
from .platforms.instagram_poster import InstagramPoster
from .platforms.linkedin_poster import LinkedInPoster
from .platforms.base import SocialMediaPoster
from .config.settings import Settings
from .utils.logger import setup_logger
from .utils.media_handler import MediaHandler


class AutomationManager:
    """Manage posting across multiple social media platforms"""

    def __init__(self, settings: Optional[Settings] = None, log_level: str = "INFO"):
        """
        Initialize automation manager
        
        Args:
            settings: Settings object with credentials (creates default if None)
            log_level: Logging level
        """
        self.settings = settings or Settings()
        self.logger = setup_logger("AutomationManager", log_level)
        self.media_handler = MediaHandler(self.settings.media_folder)
        self.platforms: Dict[str, SocialMediaPoster] = {}
        
        # Initialize available platforms
        self._initialize_platforms()

    def _initialize_platforms(self) -> None:
        """Initialize platform posters based on available credentials"""
        # Twitter
        if self.settings.has_twitter_credentials():
            try:
                twitter = TwitterPoster(
                    api_key=self.settings.twitter_api_key,
                    api_secret=self.settings.twitter_api_secret,
                    access_token=self.settings.twitter_access_token,
                    access_token_secret=self.settings.twitter_access_token_secret,
                    bearer_token=self.settings.twitter_bearer_token
                )
                if twitter.authenticate():
                    self.platforms['twitter'] = twitter
                    self.logger.info("Twitter platform initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Twitter: {e}")

        # Facebook
        if self.settings.has_facebook_credentials():
            try:
                facebook = FacebookPoster(
                    access_token=self.settings.facebook_access_token,
                    page_id=self.settings.facebook_page_id
                )
                if facebook.authenticate():
                    self.platforms['facebook'] = facebook
                    self.logger.info("Facebook platform initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Facebook: {e}")

        # Instagram
        if self.settings.has_instagram_credentials():
            try:
                instagram = InstagramPoster(
                    username=self.settings.instagram_username,
                    password=self.settings.instagram_password
                )
                if instagram.authenticate():
                    self.platforms['instagram'] = instagram
                    self.logger.info("Instagram platform initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Instagram: {e}")

        # LinkedIn
        if self.settings.has_linkedin_credentials():
            try:
                linkedin = LinkedInPoster(
                    access_token=self.settings.linkedin_access_token,
                    person_urn=self.settings.linkedin_person_urn
                )
                if linkedin.authenticate():
                    self.platforms['linkedin'] = linkedin
                    self.logger.info("LinkedIn platform initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize LinkedIn: {e}")

        if not self.platforms:
            self.logger.warning("No platforms initialized. Please check credentials.")

    def get_available_platforms(self) -> List[str]:
        """Get list of available (initialized) platforms"""
        return list(self.platforms.keys())

    def post_to_all(
        self,
        text: str,
        image_path: Optional[str] = None,
        video_path: Optional[str] = None,
        image_paths: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Post to all available platforms
        
        Args:
            text: Text content for the post
            image_path: Path to single image (optional)
            video_path: Path to video (optional)
            image_paths: List of image paths for multiple images (optional)
            
        Returns:
            Dict with results from each platform
        """
        results = {}
        
        for platform_name, platform in self.platforms.items():
            try:
                if image_paths:
                    result = platform.post_multiple_images(text, image_paths)
                elif image_path:
                    result = platform.post_image(text, image_path)
                elif video_path:
                    result = platform.post_video(text, video_path)
                else:
                    result = platform.post_text(text)
                
                results[platform_name] = result
            except Exception as e:
                self.logger.error(f"Error posting to {platform_name}: {e}")
                results[platform_name] = {
                    'success': False,
                    'platform': platform_name,
                    'error': str(e)
                }
        
        return results

    def post_to_platforms(
        self,
        platforms: List[str],
        text: str,
        image_path: Optional[str] = None,
        video_path: Optional[str] = None,
        image_paths: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Post to specific platforms
        
        Args:
            platforms: List of platform names to post to
            text: Text content for the post
            image_path: Path to single image (optional)
            video_path: Path to video (optional)
            image_paths: List of image paths for multiple images (optional)
            
        Returns:
            Dict with results from each platform
        """
        results = {}
        
        for platform_name in platforms:
            if platform_name not in self.platforms:
                self.logger.warning(f"Platform not available: {platform_name}")
                results[platform_name] = {
                    'success': False,
                    'platform': platform_name,
                    'error': 'Platform not initialized or not available'
                }
                continue
            
            platform = self.platforms[platform_name]
            try:
                if image_paths:
                    result = platform.post_multiple_images(text, image_paths)
                elif image_path:
                    result = platform.post_image(text, image_path)
                elif video_path:
                    result = platform.post_video(text, video_path)
                else:
                    result = platform.post_text(text)
                
                results[platform_name] = result
            except Exception as e:
                self.logger.error(f"Error posting to {platform_name}: {e}")
                results[platform_name] = {
                    'success': False,
                    'platform': platform_name,
                    'error': str(e)
                }
        
        return results

    def get_platform_status(self) -> Dict[str, bool]:
        """
        Get authentication status of all platforms
        
        Returns:
            Dict mapping platform names to authentication status
        """
        return {
            name: platform.authenticated
            for name, platform in self.platforms.items()
        }
