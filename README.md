# Social Media Automation Tool 🚀

Automate posting to multiple social media platforms (Twitter/X, Facebook, Instagram, LinkedIn) with a single unified interface. Schedule posts, manage media, and streamline your social media workflow.

## Features ✨

- **Multi-Platform Support**: Post to Twitter/X, Facebook, Instagram, and LinkedIn
- **Unified Interface**: One API to rule them all
- **Media Handling**: Support for images, videos, and multiple images (carousel/album)
- **Scheduling**: Schedule posts for specific times and intervals
- **CLI Interface**: Easy-to-use command-line interface
- **Python API**: Use as a Python library in your own projects
- **Logging**: Comprehensive logging with color support
- **Configuration**: Simple .env file configuration

## Supported Platforms 📱

| Platform | Text Posts | Single Image | Multiple Images | Video |
|----------|-----------|--------------|-----------------|-------|
| Twitter/X | ✅ | ✅ | ✅ (up to 4) | ✅ |
| Facebook | ✅ | ✅ | ✅ | ✅ |
| Instagram | ❌* | ✅ | ✅ (up to 10) | ✅ |
| LinkedIn | ✅ | ✅ | ✅ (up to 9) | ⚠️** |

*Instagram requires at least one image or video
**LinkedIn video upload requires additional implementation

## Installation 🔧

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Pranesh25/Automate_SocialMedia.git
   cd Automate_SocialMedia
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials:**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your social media API credentials.

## Configuration 🔑

### Getting API Credentials

#### Twitter/X
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new App
3. Generate API keys and access tokens
4. Add to `.env`: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`, `TWITTER_BEARER_TOKEN`

#### Facebook
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new App
3. Get a Page Access Token
4. Add to `.env`: `FACEBOOK_ACCESS_TOKEN`, `FACEBOOK_PAGE_ID`

#### Instagram
1. Use your Instagram username and password
2. Add to `.env`: `INSTAGRAM_USERNAME`, `INSTAGRAM_PASSWORD`
3. Note: May require 2FA setup

#### LinkedIn
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new App
3. Generate access token with proper permissions
4. Add to `.env`: `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN`

## Usage 💻

### Command Line Interface

#### Check available platforms:
```bash
python main.py list-platforms
```

#### Check authentication status:
```bash
python main.py status
```

#### Post text to all platforms:
```bash
python main.py post -t "Hello, world! 🌍 #automation"
```

#### Post with image to specific platforms:
```bash
python main.py post -t "Check this out!" -i ./media/image.jpg -p twitter facebook
```

#### Post with video:
```bash
python main.py post -t "Watch this video!" -v ./media/video.mp4 -p twitter
```

#### Post with multiple images:
```bash
python main.py post -t "Photo album!" -m ./media/img1.jpg ./media/img2.jpg ./media/img3.jpg
```

### Python API

#### Basic Example:
```python
from social_media_automation import AutomationManager, Settings

# Initialize
settings = Settings()
manager = AutomationManager(settings)

# Post to all platforms
results = manager.post_to_all(
    text="Hello from Python! 🐍"
)

# Check results
for platform, result in results.items():
    if result['success']:
        print(f"✓ Posted to {platform}: {result['url']}")
```

#### Post with Image:
```python
results = manager.post_to_platforms(
    platforms=['twitter', 'facebook'],
    text="Check out this image!",
    image_path="./media/photo.jpg"
)
```

#### Schedule Posts:
```python
from social_media_automation.scheduler import PostScheduler

scheduler = PostScheduler()

def my_post():
    manager.post_to_all(text="Scheduled post!")

# Post every day at 9 AM
scheduler.schedule_post(my_post, "09:00")

# Run scheduler
scheduler.run_continuously()
```

## Examples 📚

Check the `examples/` directory for more usage examples:

- `basic_post.py` - Simple text posting
- `post_with_image.py` - Posting with images
- `post_multiple_images.py` - Carousel/album posts
- `scheduled_posts.py` - Scheduling automated posts

Run examples:
```bash
python examples/basic_post.py
```

## Project Structure 📁

```
Automate_SocialMedia/
├── social_media_automation/       # Main package
│   ├── platforms/                 # Platform-specific implementations
│   │   ├── base.py               # Base class for all platforms
│   │   ├── twitter_poster.py     # Twitter/X implementation
│   │   ├── facebook_poster.py    # Facebook implementation
│   │   ├── instagram_poster.py   # Instagram implementation
│   │   └── linkedin_poster.py    # LinkedIn implementation
│   ├── utils/                     # Utility modules
│   │   ├── logger.py             # Logging configuration
│   │   └── media_handler.py      # Media file handling
│   ├── config/                    # Configuration management
│   │   └── settings.py           # Settings from environment
│   ├── scheduler.py               # Post scheduling
│   └── automation_manager.py      # Central manager
├── examples/                      # Usage examples
├── media/                         # Media files directory
├── main.py                        # CLI interface
├── requirements.txt               # Dependencies
├── .env.example                   # Example environment file
└── README.md                      # This file
```

## Dependencies 📦

- `tweepy` - Twitter API
- `facebook-sdk` - Facebook API
- `instagrapi` - Instagram API
- `linkedin-api` - LinkedIn API
- `python-dotenv` - Environment configuration
- `requests` - HTTP requests
- `Pillow` - Image processing
- `schedule` - Job scheduling
- `colorlog` - Colored logging

## Troubleshooting 🔧

### Authentication Issues
- Verify all credentials in `.env` are correct
- Check API token permissions
- Ensure tokens haven't expired

### Instagram Login Issues
- Instagram may require 2FA verification
- Use app-specific passwords if available
- Rate limiting may apply

### Media Upload Issues
- Check file formats are supported
- Verify file sizes are within platform limits
- Ensure file paths are correct

## Best Practices 🎯

1. **Rate Limiting**: Be mindful of API rate limits for each platform
2. **Content Guidelines**: Follow each platform's content policies
3. **Media Optimization**: Optimize images/videos before uploading
4. **Error Handling**: Always check results for errors
5. **Testing**: Test with one platform before posting to all
6. **Credentials Security**: Never commit `.env` file to version control

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is open source and available under the MIT License.

## Disclaimer ⚠️

This tool is for educational and automation purposes. Always comply with each platform's Terms of Service and API usage policies. Use responsibly and respect rate limits.

## Support 💬

For issues, questions, or contributions, please open an issue on GitHub.

---

Made with ❤️ by Pranesh25