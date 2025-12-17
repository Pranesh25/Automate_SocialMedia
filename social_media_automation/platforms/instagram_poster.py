"""Instagram platform poster implementation"""

from typing import Dict, Any, List
from instagrapi import Client
from .base import SocialMediaPoster


class InstagramPoster(SocialMediaPoster):
    """Handle posting to Instagram"""

    def __init__(self, username: str, password: str):
        """
        Initialize Instagram poster
        
        Args:
            username: Instagram username
            password: Instagram password
        """
        super().__init__("Instagram")
        self.username = username
        self.password = password
        self.client = Client()

    def authenticate(self) -> bool:
        """Authenticate with Instagram"""
        try:
            self.client.login(self.username, self.password)
            self.authenticated = True
            self.logger.info(f"Successfully authenticated with Instagram as {self.username}")
            return True
        except Exception as e:
            self.logger.error(f"Instagram authentication failed: {e}")
            self.authenticated = False
            return False

    def post_text(self, text: str) -> Dict[str, Any]:
        """
        Instagram doesn't support text-only posts
        This will return an error
        """
        self.logger.error("Instagram does not support text-only posts")
        return {
            'success': False,
            'platform': self.platform_name,
            'error': 'Instagram requires at least one image or video'
        }

    def post_image(self, text: str, image_path: str) -> Dict[str, Any]:
        """Post photo to Instagram"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            media = self.client.photo_upload(
                image_path,
                caption=text
            )
            self.logger.info(f"Posted photo to Instagram: {media.pk}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': media.pk,
                'url': f"https://www.instagram.com/p/{media.code}/"
            }
        except Exception as e:
            self.logger.error(f"Failed to post photo to Instagram: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_video(self, text: str, video_path: str) -> Dict[str, Any]:
        """Post video to Instagram"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            media = self.client.video_upload(
                video_path,
                caption=text
            )
            self.logger.info(f"Posted video to Instagram: {media.pk}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': media.pk,
                'url': f"https://www.instagram.com/p/{media.code}/"
            }
        except Exception as e:
            self.logger.error(f"Failed to post video to Instagram: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_multiple_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """Post album/carousel with multiple images to Instagram"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            # Instagram allows up to 10 images in a carousel
            image_paths = image_paths[:10]
            
            media = self.client.album_upload(
                image_paths,
                caption=text
            )
            self.logger.info(f"Posted album with {len(image_paths)} images to Instagram: {media.pk}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': media.pk,
                'url': f"https://www.instagram.com/p/{media.code}/",
                'media_count': len(image_paths)
            }
        except Exception as e:
            self.logger.error(f"Failed to post album to Instagram: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }
