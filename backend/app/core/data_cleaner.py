import re
import logging
from typing import List, Dict, Any

from app.models.tweet import Tweet

class DataCleaner:
    """Class for cleaning and preprocessing tweet data."""
    
    def __init__(self):
        """Initialize data cleaner."""
        self.logger = logging.getLogger(__name__)
    
    def clean_tweets(self, tweets: List[Tweet]) -> List[Tweet]:
        """
        Clean a list of tweets.
        
        Args:
            tweets: List of Tweet objects
            
        Returns:
            Cleaned list of Tweet objects
        """
        cleaned_tweets = []
        seen_ids = set()
        
        for tweet in tweets:
            # Skip if ID already seen (duplicate)
            if tweet.id in seen_ids:
                continue
                
            # Clean text
            cleaned_text = self.clean_text(tweet.text)
            
            # Skip if text is empty after cleaning
            if not cleaned_text:
                continue
                
            # Update tweet with cleaned text
            tweet.text = cleaned_text
            
            # Add to result and mark as seen
            cleaned_tweets.append(tweet)
            seen_ids.add(tweet.id)
        
        self.logger.info(f"Cleaned {len(tweets)} tweets, resulting in {len(cleaned_tweets)} valid tweets")
        return cleaned_tweets
    
    def clean_text(self, text: str) -> str:
        """
        Clean tweet text.
        
        Args:
            text: Raw tweet text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Remove URLs
        text = re.sub(r'https?://\\S+|www\\.\\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove usernames
        text = re.sub(r'@\\w+', '', text)
        
        # Remove hashtag symbol but keep the text
        text = re.sub(r'#(\\w+)', r'\\1', text)
        
        # Remove extra whitespace
        text = re.sub(r'\\s+', ' ', text)
        
        # Strip whitespace
        text = text.strip()
        
        return text