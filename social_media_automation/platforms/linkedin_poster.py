"""LinkedIn platform poster implementation"""

from typing import Dict, Any, List
import requests
import json
from .base import SocialMediaPoster


class LinkedInPoster(SocialMediaPoster):
    """Handle posting to LinkedIn"""

    def __init__(self, access_token: str, person_urn: str):
        """
        Initialize LinkedIn poster
        
        Args:
            access_token: LinkedIn access token
            person_urn: LinkedIn person URN (e.g., 'urn:li:person:XXXXXXXXX')
        """
        super().__init__("LinkedIn")
        self.access_token = access_token
        self.person_urn = person_urn
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

    def authenticate(self) -> bool:
        """Verify LinkedIn credentials"""
        try:
            # Verify the access token by getting user info
            url = f"{self.base_url}/me"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            user_data = response.json()
            self.authenticated = True
            self.logger.info(f"Successfully authenticated with LinkedIn")
            return True
        except Exception as e:
            self.logger.error(f"LinkedIn authentication failed: {e}")
            self.authenticated = False
            return False

    def post_text(self, text: str) -> Dict[str, Any]:
        """Post text-only update to LinkedIn"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            url = f"{self.base_url}/ugcPosts"
            
            post_data = {
                "author": self.person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(url, headers=self.headers, data=json.dumps(post_data))
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            self.logger.info(f"Posted to LinkedIn: {post_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': post_id,
                'url': f"https://www.linkedin.com/feed/update/{post_id}/"
            }
        except Exception as e:
            self.logger.error(f"Failed to post to LinkedIn: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def _upload_image(self, image_path: str) -> str:
        """
        Upload image to LinkedIn and return asset URN
        
        Args:
            image_path: Path to image file
            
        Returns:
            Asset URN of uploaded image
        """
        # Step 1: Register upload
        register_url = f"{self.base_url}/assets?action=registerUpload"
        register_data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": self.person_urn,
                "serviceRelationships": [{
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }]
            }
        }
        
        response = requests.post(register_url, headers=self.headers, data=json.dumps(register_data))
        response.raise_for_status()
        result = response.json()
        
        upload_url = result['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset = result['value']['asset']
        
        # Step 2: Upload image
        with open(image_path, 'rb') as image_file:
            upload_headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            response = requests.put(upload_url, headers=upload_headers, data=image_file)
            response.raise_for_status()
        
        return asset

    def post_image(self, text: str, image_path: str) -> Dict[str, Any]:
        """Post image with text to LinkedIn"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            # Upload image and get asset URN
            asset_urn = self._upload_image(image_path)
            
            # Create post with image
            url = f"{self.base_url}/ugcPosts"
            post_data = {
                "author": self.person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [{
                            "status": "READY",
                            "media": asset_urn
                        }]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(url, headers=self.headers, data=json.dumps(post_data))
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            self.logger.info(f"Posted image to LinkedIn: {post_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': post_id,
                'url': f"https://www.linkedin.com/feed/update/{post_id}/"
            }
        except Exception as e:
            self.logger.error(f"Failed to post image to LinkedIn: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }

    def post_video(self, text: str, video_path: str) -> Dict[str, Any]:
        """Post video to LinkedIn (similar to image upload but more complex)"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        self.logger.warning("Video upload to LinkedIn is complex and requires chunked upload")
        return {
            'success': False,
            'platform': self.platform_name,
            'error': 'Video upload not fully implemented - requires chunked upload process'
        }

    def post_multiple_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """Post multiple images to LinkedIn"""
        if not self.authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")

        try:
            # Upload all images and collect asset URNs
            media_assets = []
            for image_path in image_paths[:9]:  # LinkedIn allows up to 9 images
                asset_urn = self._upload_image(image_path)
                media_assets.append({
                    "status": "READY",
                    "media": asset_urn
                })
            
            # Create post with multiple images
            url = f"{self.base_url}/ugcPosts"
            post_data = {
                "author": self.person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": media_assets
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(url, headers=self.headers, data=json.dumps(post_data))
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            self.logger.info(f"Posted {len(media_assets)} images to LinkedIn: {post_id}")
            return {
                'success': True,
                'platform': self.platform_name,
                'post_id': post_id,
                'url': f"https://www.linkedin.com/feed/update/{post_id}/",
                'media_count': len(media_assets)
            }
        except Exception as e:
            self.logger.error(f"Failed to post multiple images to LinkedIn: {e}")
            return {
                'success': False,
                'platform': self.platform_name,
                'error': str(e)
            }
