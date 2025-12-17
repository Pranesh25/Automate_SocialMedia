"""Scheduler for automated social media posting"""

import schedule
import time
from typing import List, Dict, Any, Callable
from datetime import datetime
import logging


class PostScheduler:
    """Schedule social media posts"""

    def __init__(self):
        """Initialize the scheduler"""
        self.logger = logging.getLogger(__name__)
        self.jobs = []

    def schedule_post(
        self,
        post_function: Callable,
        time_str: str,
        *args,
        **kwargs
    ) -> None:
        """
        Schedule a post at a specific time
        
        Args:
            post_function: Function to call for posting
            time_str: Time string in HH:MM format (24-hour)
            *args: Arguments to pass to post_function
            **kwargs: Keyword arguments to pass to post_function
        """
        job = schedule.every().day.at(time_str).do(
            post_function,
            *args,
            **kwargs
        )
        self.jobs.append(job)
        self.logger.info(f"Scheduled post at {time_str}")

    def schedule_interval_post(
        self,
        post_function: Callable,
        interval_hours: int,
        *args,
        **kwargs
    ) -> None:
        """
        Schedule a post to repeat at regular intervals
        
        Args:
            post_function: Function to call for posting
            interval_hours: Interval in hours between posts
            *args: Arguments to pass to post_function
            **kwargs: Keyword arguments to pass to post_function
        """
        job = schedule.every(interval_hours).hours.do(
            post_function,
            *args,
            **kwargs
        )
        self.jobs.append(job)
        self.logger.info(f"Scheduled post every {interval_hours} hours")

    def schedule_weekly_post(
        self,
        post_function: Callable,
        day: str,
        time_str: str,
        *args,
        **kwargs
    ) -> None:
        """
        Schedule a post on a specific day of the week
        
        Args:
            post_function: Function to call for posting
            day: Day of week (monday, tuesday, etc.)
            time_str: Time string in HH:MM format (24-hour)
            *args: Arguments to pass to post_function
            **kwargs: Keyword arguments to pass to post_function
        """
        day_schedule = getattr(schedule.every(), day.lower())
        job = day_schedule.at(time_str).do(
            post_function,
            *args,
            **kwargs
        )
        self.jobs.append(job)
        self.logger.info(f"Scheduled post every {day} at {time_str}")

    def clear_all_jobs(self) -> None:
        """Clear all scheduled jobs"""
        schedule.clear()
        self.jobs = []
        self.logger.info("Cleared all scheduled jobs")

    def get_next_run(self) -> Dict[str, Any]:
        """
        Get information about the next scheduled run
        
        Returns:
            Dict with next run information
        """
        if not self.jobs:
            return {'next_run': None, 'job_count': 0}
        
        next_job = min(self.jobs, key=lambda j: j.next_run)
        return {
            'next_run': next_job.next_run,
            'job_count': len(self.jobs),
            'time_until': (next_job.next_run - datetime.now()).total_seconds()
        }

    def run_pending(self) -> None:
        """Run all pending scheduled jobs"""
        schedule.run_pending()

    def run_continuously(self, interval: int = 1) -> None:
        """
        Run the scheduler continuously
        
        Args:
            interval: Check interval in seconds
        """
        self.logger.info(f"Starting continuous scheduler (checking every {interval}s)")
        try:
            while True:
                schedule.run_pending()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")

    def list_jobs(self) -> List[str]:
        """
        List all scheduled jobs
        
        Returns:
            List of job descriptions
        """
        return [str(job) for job in self.jobs]
