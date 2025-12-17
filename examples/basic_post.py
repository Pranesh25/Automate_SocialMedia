#!/usr/bin/env python3
"""
Example: Basic text post to all platforms
"""

from social_media_automation import AutomationManager, Settings, setup_logger

# Set up logging
logger = setup_logger("Example", "INFO")

# Initialize the automation manager with settings from .env file
settings = Settings()
manager = AutomationManager(settings)

# Check available platforms
available_platforms = manager.get_available_platforms()
logger.info(f"Available platforms: {available_platforms}")

if not available_platforms:
    logger.error("No platforms configured. Please set up credentials in .env file")
    exit(1)

# Post text to all available platforms
text = "Hello from Social Media Automation! 🚀 #automation #socialmedia"

results = manager.post_to_all(text=text)

# Display results
logger.info("\n=== Results ===")
for platform, result in results.items():
    if result['success']:
        logger.info(f"✓ {platform}: {result.get('url')}")
    else:
        logger.error(f"✗ {platform}: {result.get('error')}")
