#!/usr/bin/env python3
"""
Example: Post with multiple images (carousel/album)
"""

from social_media_automation import AutomationManager, Settings, setup_logger

# Set up logging
logger = setup_logger("Example", "INFO")

# Initialize the automation manager
settings = Settings()
manager = AutomationManager(settings)

# Post with multiple images
text = "Check out these amazing photos! 🎨📸 #photography #carousel #album"
image_paths = [
    "../media/image1.jpg",  # Replace with your image paths
    "../media/image2.jpg",
    "../media/image3.jpg"
]

# Post to all platforms
results = manager.post_to_all(
    text=text,
    image_paths=image_paths
)

# Display results
logger.info("\n=== Results ===")
for platform, result in results.items():
    if result['success']:
        logger.info(f"✓ {platform}: {result.get('url')}")
        if 'media_count' in result:
            logger.info(f"  Images posted: {result['media_count']}")
    else:
        logger.error(f"✗ {platform}: {result.get('error')}")
