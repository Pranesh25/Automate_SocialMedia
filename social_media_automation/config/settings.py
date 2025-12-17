"""Configuration management using environment variables"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


class Settings:
    """Manage application settings from environment variables"""

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize settings from environment variables
        
        Args:
            env_file: Path to .env file (uses default if None)
        """
        # Load .env file if it exists
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to find .env in current directory or parent directories
            load_dotenv()

        # Twitter/X credentials
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

        # Facebook credentials
        self.facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.facebook_page_id = os.getenv('FACEBOOK_PAGE_ID')

        # Instagram credentials
        self.instagram_username = os.getenv('INSTAGRAM_USERNAME')
        self.instagram_password = os.getenv('INSTAGRAM_PASSWORD')

        # LinkedIn credentials
        self.linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_person_urn = os.getenv('LINKEDIN_PERSON_URN')

        # General settings
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.media_folder = os.getenv('MEDIA_FOLDER', './media')

    def has_twitter_credentials(self) -> bool:
        """Check if Twitter credentials are configured"""
        return all([
            self.twitter_api_key,
            self.twitter_api_secret,
            self.twitter_access_token,
            self.twitter_access_token_secret
        ])

    def has_facebook_credentials(self) -> bool:
        """Check if Facebook credentials are configured"""
        return all([
            self.facebook_access_token,
            self.facebook_page_id
        ])

    def has_instagram_credentials(self) -> bool:
        """Check if Instagram credentials are configured"""
        return all([
            self.instagram_username,
            self.instagram_password
        ])

    def has_linkedin_credentials(self) -> bool:
        """Check if LinkedIn credentials are configured"""
        return all([
            self.linkedin_access_token,
            self.linkedin_person_urn
        ])

    def get_configured_platforms(self) -> list:
        """Get list of platforms with configured credentials"""
        platforms = []
        if self.has_twitter_credentials():
            platforms.append('twitter')
        if self.has_facebook_credentials():
            platforms.append('facebook')
        if self.has_instagram_credentials():
            platforms.append('instagram')
        if self.has_linkedin_credentials():
            platforms.append('linkedin')
        return platforms
