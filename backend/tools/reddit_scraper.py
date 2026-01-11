import praw
from typing import List, Dict, Optional
from config import settings


class RedditScraper:
    def __init__(self):
        self.reddit = None
        if settings.reddit_client_id and settings.reddit_client_secret:
            self.reddit = praw.Reddit(
                client_id=settings.reddit_client_id,
                client_secret=settings.reddit_client_secret,
                user_agent=settings.reddit_user_agent
            )
    
    def search_posts(self, query: str, subreddit: str = "all", limit: int = 10) -> List[Dict]:
        if not self.reddit:
            return []
        
        posts = []
        try:
            subreddit_obj = self.reddit.subreddit(subreddit)
            
            for submission in subreddit_obj.search(query, limit=limit, sort='relevance'):
                posts.append({
                    "title": submission.title,
                    "text": submission.selftext,
                    "score": submission.score,
                    "url": submission.url,
                    "created_utc": submission.created_utc,
                    "num_comments": submission.num_comments,
                    "subreddit": str(submission.subreddit)
                })
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
        
        return posts
    
    def get_comments(self, post_url: str, limit: int = 20) -> List[str]:
        if not self.reddit:
            return []
        
        comments = []
        try:
            submission = self.reddit.submission(url=post_url)
            submission.comments.replace_more(limit=0)
            
            for comment in submission.comments.list()[:limit]:
                if hasattr(comment, 'body'):
                    comments.append(comment.body)
        except Exception as e:
            print(f"Error getting comments: {e}")
        
        return comments
