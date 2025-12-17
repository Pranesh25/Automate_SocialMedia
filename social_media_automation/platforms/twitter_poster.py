"""Twitter/X platform poster implementation"""

from typing import Dict, Any, List
import tweepy
from .base import SocialMediaPoster


class TwitterPoster(SocialMediaPoster):
    """Handle posting to Twitter/X"""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_token_secret: str,
        bearer_token: str = None
    ):
        """
        Initialize Twitter poster
        
        Args:
            api_key: Twitter API key
            api_secret: Twitter API secret
            access_token: Twitter access token
            access_token_secret: Twitter access token secret
            bearer_token: Optional bearer token for API v2
        """
        super().__init__("Twitter")
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.bearer_token = bearer_token
        self.client = None
        self.api = None

    def authenticate(self) -> bool:
        """Authenticate with Twitter API"""
        try:
            # API v2 client
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )

            # API v1.1 for media upload
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api = tweepy.API(auth)

            # Verify credentials
            self.client.get_me()
            self.authenticated = True
            self.logger.info("Successfully authenticated with Twitter")
            return True
        except Exception as e:
            self.logger.error(f"Twitter authentication failed: {e}")
            self.authenticated = False
            return False

    def post_text(self, text: str) -> Dict[str, Any]:
        """Post text-only tweet"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            self.logger.info(f"Posted tweet: {tweet_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': tweet_id,
                'url': f"https://twitter.com/user/status/{tweet_id}"
            }
        except Exception as e:
            self.logger.error(f"Failed to post tweet: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_image(self, text: str, image_path: str) -> Dict[str, Any]:
        """Post tweet with image"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            # Upload media using API v1.1
            media = self.api.media_upload(filename=image_path)
            
            # Create tweet with media using API v2
            response = self.client.create_tweet(
                text=text,
                media_ids=[media.media_id]
            )
            tweet_id = response.data['id']
            self.logger.info(f"Posted tweet with image: {tweet_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': tweet_id,
                'url': f"https://twitter.com/user/status/{tweet_id}"
            }
        except Exception as e:
            self.logger.error(f"Failed to post tweet with image: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_video(self, text: str, video_path: str) -> Dict[str, Any]:
        """Post tweet with video"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            # Upload media using API v1.1
            media = self.api.media_upload(filename=video_path)
            
            # Create tweet with media using API v2
            response = self.client.create_tweet(
                text=text,
                media_ids=[media.media_id]
            )
            tweet_id = response.data['id']
            self.logger.info(f"Posted tweet with video: {tweet_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': tweet_id,
                'url': f"https://twitter.com/user/status/{tweet_id}"
            }
        except Exception as e:
            self.logger.error(f"Failed to post tweet with video: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_multiple_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """Post tweet with multiple images (up to 4)"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            # Twitter allows up to 4 images
            image_paths = image_paths[:4]
            
            # Upload all media files
            media_ids = []
            for image_path in image_paths:
                media = self.api.media_upload(filename=image_path)
                media_ids.append(media.media_id)
            
            # Create tweet with multiple media
            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids
            )
            tweet_id = response.data['id']
            self.logger.info(f"Posted tweet with {len(media_ids)} images: {tweet_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': tweet_id,
                'url': f"https://twitter.com/user/status/{tweet_id}",
                'media_count': len(media_ids)
            }
        except Exception as e:
            self.logger.error(f"Failed to post tweet with multiple images: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }
