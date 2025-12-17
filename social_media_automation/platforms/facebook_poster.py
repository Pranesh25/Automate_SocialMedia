"""Facebook platform poster implementation"""

from typing import Dict, Any, List
import requests
from .base import SocialMediaPoster


class FacebookPoster(SocialMediaPoster):
    """Handle posting to Facebook"""

    def __init__(self, access_token: str, page_id: str, api_version: str = "v18.0"):
        """
        Initialize Facebook poster
        
        Args:
            access_token: Facebook page access token
            page_id: Facebook page ID
            api_version: Facebook Graph API version (default: v18.0)
        """
        super().__init__("Facebook")
        self.access_token = access_token
        self.page_id = page_id
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def authenticate(self) -> bool:
        """Verify Facebook credentials"""
        try:
            # Verify the access token by getting page info
            url = f"{self.base_url}/{self.page_id}"
            params = {
                'access_token': self.access_token,
                'fields': 'id,name'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            page_data = response.json()
            self.authenticated = True
            self.logger.info(f"Successfully authenticated with Facebook page: {page_data.get('name')}")
            return True
        except Exception as e:
            self.logger.error(f"Facebook authentication failed: {e}")
            self.authenticated = False
            return False

    def post_text(self, text: str) -> Dict[str, Any]:
        """Post text-only status to Facebook"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            url = f"{self.base_url}/{self.page_id}/feed"
            data = {
                'message': text,
                'access_token': self.access_token
            }
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            self.logger.info(f"Posted to Facebook: {post_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': post_id,
                'url': f"https://www.facebook.com/{post_id}"
            }
        except Exception as e:
            self.logger.error(f"Failed to post to Facebook: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_image(self, text: str, image_path: str) -> Dict[str, Any]:
        """Post photo to Facebook"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            url = f"{self.base_url}/{self.page_id}/photos"
            
            with open(image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'message': text,
                    'access_token': self.access_token
                }
                response = requests.post(url, data=data, files=files)
                response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            self.logger.info(f"Posted photo to Facebook: {post_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': post_id,
                'url': f"https://www.facebook.com/{post_id}"
            }
        except Exception as e:
            self.logger.error(f"Failed to post photo to Facebook: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_video(self, text: str, video_path: str) -> Dict[str, Any]:
        """Post video to Facebook"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            url = f"{self.base_url}/{self.page_id}/videos"
            
            with open(video_path, 'rb') as video_file:
                files = {'source': video_file}
                data = {
                    'description': text,
                    'access_token': self.access_token
                }
                response = requests.post(url, data=data, files=files)
                response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            self.logger.info(f"Posted video to Facebook: {post_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': post_id,
                'url': f"https://www.facebook.com/{post_id}"
            }
        except Exception as e:
            self.logger.error(f"Failed to post video to Facebook: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_multiple_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """Post multiple photos to Facebook as an album"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            # First, upload all photos without publishing
            photo_ids = []
            for image_path in image_paths:
                url = f"{self.base_url}/{self.page_id}/photos"
                with open(image_path, 'rb') as image_file:
                    files = {'source': image_file}
                    data = {
                        'published': 'false',
                        'access_token': self.access_token
                    }
                    response = requests.post(url, data=data, files=files)
                    response.raise_for_status()
                    photo_ids.append({'media_fbid': response.json()['id']})
            
            # Then create a post with all photos
            url = f"{self.base_url}/{self.page_id}/feed"
            data = {
                'message': text,
                'attached_media': str(photo_ids).replace("'", '"'),
                'access_token': self.access_token
            }
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            self.logger.info(f"Posted {len(photo_ids)} photos to Facebook: {post_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': post_id,
                'url': f"https://www.facebook.com/{post_id}",
                'media_count': len(photo_ids)
            }
        except Exception as e:
            self.logger.error(f"Failed to post multiple photos to Facebook: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }
