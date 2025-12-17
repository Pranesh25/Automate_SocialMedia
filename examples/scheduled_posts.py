#!/usr/bin/env python3
"""
Example: Schedule automated posts
"""

from social_media_automation import AutomationManager, Settings, setup_logger
from social_media_automation.scheduler import PostScheduler

# Set up logging
logger = setup_logger("ScheduledExample", "INFO")

# Initialize the automation manager
settings = Settings()
manager = AutomationManager(settings)
scheduler = PostScheduler()

# Define a function to post content
def post_daily_update():
    text = "Daily update: Automation is working great! 🎯 #daily #automation"
    results = manager.post_to_all(text=text)
    
    for platform, result in results.items():
        if result['success']:
            logger.info(f"✓ Posted to {platform}")
        else:
            logger.error(f"✗ Failed to post to {platform}: {result.get('error')}")

def post_weekly_summary():
    text = "Weekly summary: Another successful week of automated posting! 📊 #weekly #summary"
    results = manager.post_to_all(text=text)
    
    for platform, result in results.items():
        if result['success']:
            logger.info(f"✓ Posted weekly summary to {platform}")

# Schedule posts
# Post every day at 9:00 AM
scheduler.schedule_post(post_daily_update, "09:00")

# Post every Monday at 5:00 PM
scheduler.schedule_weekly_post(post_weekly_summary, "monday", "17:00")

# Show scheduled jobs
logger.info("Scheduled jobs:")
for job in scheduler.list_jobs():
    logger.info(f"  - {job}")

# Show next run time
next_run_info = scheduler.get_next_run()
logger.info(f"\nNext scheduled run: {next_run_info['next_run']}")
logger.info(f"Total jobs: {next_run_info['job_count']}")

# Run the scheduler (this will run indefinitely)
logger.info("\nStarting scheduler... (Press Ctrl+C to stop)")
try:
    scheduler.run_continuously(interval=60)  # Check every 60 seconds
except KeyboardInterrupt:
    logger.info("Scheduler stopped by user")
