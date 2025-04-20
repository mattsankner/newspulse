import re
import logging
from typing import List, Dict, Any

from app.models.article import Article

class DataCleaner:
    """Class for cleaning and preprocessing article data."""
    
    def __init__(self):
        """Initialize data cleaner."""
        self.logger = logging.getLogger(__name__)
    
    def clean_articles(self, articles: List[Article]) -> List[Article]:
        """
        Clean a list of articles.
        
        Args:
            articles: List of Article objects
            
        Returns:
            Cleaned list of Article objects
        """
        cleaned_articles = []
        seen_ids = set()
        
        for article in articles:
            # Skip if ID already seen (duplicate)
            if article.id in seen_ids:
                continue
                
            # Clean title and content
            cleaned_title = self.clean_text(article.title)
            cleaned_description = self.clean_text(article.description or '')
            cleaned_content = self.clean_text(article.content or '')
            
            # Skip if title is empty after cleaning
            if not cleaned_title:
                continue
                
            # Update article with cleaned text
            article.title = cleaned_title
            article.description = cleaned_description
            article.content = cleaned_content
            
            # Add to result and mark as seen
            cleaned_articles.append(article)
            seen_ids.add(article.id)
        
        self.logger.info(f"Cleaned {len(articles)} articles, resulting in {len(cleaned_articles)} valid articles")
        return cleaned_articles
    
    def clean_text(self, text: str) -> str:
        """
        Clean article text.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Handle common encoding issues
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        # Remove extra whitespace
        text = re.sub(r'\\s+', ' ', text)
        
        # Strip whitespace
        text = text.strip()
        
        return text