import tweepy
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.tweet import Tweet

class TwitterClient:
    """Client for interacting with X (Twitter) API."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        bearer_token: Optional[str] = None
    ):
        """Initialize Twitter client with API credentials."""
        self.api_key = api_key or settings.TWITTER_API_KEY
        self.api_secret = api_secret or settings.TWITTER_API_SECRET
        self.bearer_token = bearer_token or settings.TWITTER_BEARER_TOKEN
        
        if not self.bearer_token:
            raise ValueError("Twitter Bearer Token is required")
        
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            wait_on_rate_limit=True
        )
        
        self.logger = logging.getLogger(__name__)
    
    def search_recent_tweets(
        self, 
        query: str, 
        max_results: int = 100,
        days_back: int = 7
    ) -> List[Tweet]:
        """
        Search for recent tweets matching the query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            days_back: Number of days back to search
            
        Returns:
            List of Tweet objects
        """
        self.logger.info(f"Searching for tweets matching: {query}")
        
        # Calculate start time
        start_time = datetime.utcnow() - timedelta(days=days_back)
        
        # Define tweet fields to retrieve
        tweet_fields = [
            "id", "text", "author_id", "created_at", 
            "public_metrics", "entities"
        ]
        user_fields = ["id", "name", "username"]
        expansions = ["author_id"]
        
        # Search tweets
        try:
            response = self.client.search_recent_tweets(
                query=query,
                tweet_fields=tweet_fields,
                user_fields=user_fields,
                expansions=expansions,
                max_results=min(max_results, 100),  # API limit is 100 per request
                start_time=start_time
            )
        except Exception as e:
            self.logger.error(f"Error searching tweets: {e}")
            return []
        
        # Process results
        if not response.data:
            self.logger.warning(f"No tweets found for query: {query}")
            return []
        
        # Create a user lookup dictionary
        users = {user.id: user for user in response.includes.get("users", [])}
        
        # Convert to Tweet objects
        tweets = []
        for tweet_data in response.data:
            author = users.get(tweet_data.author_id)
            
            tweet = Tweet(
                id=tweet_data.id,
                text=tweet_data.text,
                author_id=tweet_data.author_id,
                author_username=author.username if author else None,
                author_name=author.name if author else None,
                created_at=tweet_data.created_at,
                retweet_count=tweet_data.public_metrics.get("retweet_count", 0),
                like_count=tweet_data.public_metrics.get("like_count", 0),
                raw_data=tweet_data.data
            )
            tweets.append(tweet)
        
        self.logger.info(f"Retrieved {len(tweets)} tweets")
        return tweets