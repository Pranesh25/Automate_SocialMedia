#!/usr/bin/env python3
"""
Main CLI for Social Media Automation
"""

import argparse
import sys
from pathlib import Path
from social_media_automation import (
    AutomationManager,
    Settings,
    setup_logger
)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Automate social media posting across multiple platforms'
    )
    
    # Action arguments
    parser.add_argument(
        'action',
        choices=['post', 'status', 'list-platforms'],
        help='Action to perform'
    )
    
    # Content arguments
    parser.add_argument(
        '-t', '--text',
        type=str,
        help='Text content for the post'
    )
    
    parser.add_argument(
        '-i', '--image',
        type=str,
        help='Path to image file'
    )
    
    parser.add_argument(
        '-v', '--video',
        type=str,
        help='Path to video file'
    )
    
    parser.add_argument(
        '-m', '--multiple-images',
        nargs='+',
        type=str,
        help='Paths to multiple image files'
    )
    
    # Platform selection
    parser.add_argument(
        '-p', '--platforms',
        nargs='+',
        choices=['twitter', 'facebook', 'instagram', 'linkedin', 'all'],
        default=['all'],
        help='Target platforms (default: all)'
    )
    
    # Configuration
    parser.add_argument(
        '--env-file',
        type=str,
        help='Path to .env file with credentials'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Initialize settings and manager
    settings = Settings(env_file=args.env_file)
    manager = AutomationManager(settings, log_level=args.log_level)
    logger = setup_logger("CLI", args.log_level)
    
    # Handle actions
    if args.action == 'list-platforms':
        platforms = manager.get_available_platforms()
        if platforms:
            logger.info(f"Available platforms: {', '.join(platforms)}")
            for platform in platforms:
                logger.info(f"  - {platform.capitalize()}")
        else:
            logger.warning("No platforms available. Please configure credentials in .env file")
        return 0
    
    elif args.action == 'status':
        status = manager.get_platform_status()
        logger.info("Platform authentication status:")
        for platform, authenticated in status.items():
            status_str = "✓ Authenticated" if authenticated else "✗ Not authenticated"
            logger.info(f"  {platform.capitalize()}: {status_str}")
        return 0
    
    elif args.action == 'post':
        if not args.text:
            logger.error("Text content is required for posting (use -t/--text)")
            return 1
        
        # Validate media files if provided
        if args.image and not Path(args.image).exists():
            logger.error(f"Image file not found: {args.image}")
            return 1
        
        if args.video and not Path(args.video).exists():
            logger.error(f"Video file not found: {args.video}")
            return 1
        
        if args.multiple_images:
            for img_path in args.multiple_images:
                if not Path(img_path).exists():
                    logger.error(f"Image file not found: {img_path}")
                    return 1
        
        # Determine which platforms to post to
        platforms = args.platforms
        if 'all' in platforms:
            platforms = manager.get_available_platforms()
        
        if not platforms:
            logger.error("No platforms available. Please configure credentials in .env file")
            return 1
        
        # Post to platforms
        logger.info(f"Posting to: {', '.join(platforms)}")
        
        results = manager.post_to_platforms(
            platforms=platforms,
            text=args.text,
            image_path=args.image,
            video_path=args.video,
            image_paths=args.multiple_images
        )
        
        # Display results
        logger.info("\n=== Post Results ===")
        for platform, result in results.items():
            if result['success']:
                logger.info(f"✓ {platform.capitalize()}: Success")
                logger.info(f"  Post ID: {result.get('post_id')}")
                logger.info(f"  URL: {result.get('url')}")
            else:
                logger.error(f"✗ {platform.capitalize()}: Failed")
                logger.error(f"  Error: {result.get('error')}")
        
        # Return error code if any post failed
        if any(not r['success'] for r in results.values()):
            return 1
        
        return 0


if __name__ == '__main__':
    sys.exit(main())
