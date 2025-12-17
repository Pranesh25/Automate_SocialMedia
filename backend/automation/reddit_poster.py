import praw
import os

class RedditPoster:
    def __init__(self, client_id, client_secret, username, password, user_agent="BlurSocialApp/1.0"):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )
        self.reddit.validate_on_submit = True

    def post_text(self, subreddit_name, title, content):
        subreddit = self.reddit.subreddit(subreddit_name)
        submission = subreddit.submit(title, selftext=content)
        return submission.permalink

    def post_image(self, subreddit_name, title, image_path):
        subreddit = self.reddit.subreddit(subreddit_name)
        submission = subreddit.submit_image(title, image_path)
        return submission.permalink

    def post_video(self, subreddit_name, title, video_path):
        subreddit = self.reddit.subreddit(subreddit_name)
        submission = subreddit.submit_video(title, video_path)
        return submission.permalink
