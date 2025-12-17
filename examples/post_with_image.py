#!/usr/bin/env python3
"""
Example: Post with image to specific platforms
"""

from social_media_automation import AutomationManager, Settings, setup_logger

# Set up logging
logger = setup_logger("Example", "INFO")

# Initialize the automation manager
settings = Settings()
manager = AutomationManager(settings)

# Post to specific platforms with an image
text = "Check out this amazing image! 📸 #photography #automation"
image_path = "../media/sample_image.jpg"  # Replace with your image path

# Post to Twitter and Facebook only
platforms = ['twitter', 'facebook']

results = manager.post_to_platforms(
    platforms=platforms,
    text=text,
    image_path=image_path
)

# Display results
logger.info("\n=== Results ===")
for platform, result in results.items():
    if result['success']:
        logger.info(f"✓ {platform}: {result.get('url')}")
    else:
        logger.error(f"✗ {platform}: {result.get('error')}")
