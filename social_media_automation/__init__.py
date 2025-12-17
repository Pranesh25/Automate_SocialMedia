"""
Social Media Automation Package
Automate posting to multiple social media platforms
"""

__version__ = "1.0.0"
__author__ = "Pranesh25"

from .platforms.base import SocialMediaPoster
from .platforms.twitter_poster import TwitterPoster
from .platforms.facebook_poster import FacebookPoster
from .platforms.instagram_poster import InstagramPoster
from .platforms.linkedin_poster import LinkedInPoster
from .utils.logger import setup_logger
from .utils.media_handler import MediaHandler
from .config.settings import Settings
from .automation_manager import AutomationManager
from .scheduler import PostScheduler

__all__ = [
    'SocialMediaPoster',
    'TwitterPoster',
    'FacebookPoster',
    'InstagramPoster',
    'LinkedInPoster',
    'setup_logger',
    'MediaHandler',
    'Settings',
    'AutomationManager',
    'PostScheduler'
]
