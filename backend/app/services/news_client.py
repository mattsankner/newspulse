import logging
from datetime import datetime, timedelta, UTC
from typing import List, Dict, Any, Optional
from newsapi import NewsApiClient
from ..core.config import settings
from ..models.article import Article

class NewsClient:
    """Client for interacting with NewsAPI."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
    ):
        """Initialize Twitter client with API credentials."""
        self.api_key = api_key or settings.NEWS_API_KEY
        
        if not self.api_key:
            raise ValueError("News API Key is required")
        
        self.client = NewsApiClient(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)
    
    def get_articles_by_topic(
        self, 
        topic: str, 
        language: str = 'en',
        days_back: int = 7,
        page_size: int = 100,
        page: int = 1
    ) -> List[Article]:
        """
        Get articles related to a political topic.
        
        Args:
            topic: Search query string
            language: Language of articles (default: 'en')
            days_back: Number of days back to search
            page_size: Number of articles per page (max 100)
            page: Page number
            
        Returns:
            List of Article objects
        """
        self.logger.info(f"Searching for articles related to: {topic}")
        
        # Calculate date range
        to_date = datetime.utcnow()
        from_date = to_date - timedelta(days=days_back)
        
        # Format dates as required by News API (YYYY-MM-DD)
        from_date_str = from_date.strftime('%Y-%m-%d')
        to_date_str = to_date.strftime('%Y-%m-%d')
        
        try:
            # Use everything endpoint to get articles
            response = self.client.get_everything(
                q=topic,
                language=language,
                from_param=from_date_str,
                to=to_date_str,
                sort_by='relevancy',
                page_size=page_size,
                page=page
            )
        except Exception as e:
            self.logger.error(f"Error fetching articles: {e}")
            return []
        
        if not response or 'articles' not in response or not response['articles']:
            self.logger.warning(f"No articles found for topic: {topic}")
            return []
        
        # Convert to Article objects
        articles = []
        for article_data in response['articles']:
            try:
                # Generate a unique ID for the article (using URL hash)
                import hashlib
                url = article_data.get('url', '')
                article_id = hashlib.md5(url.encode()).hexdigest() if url else None
                
                if not article_id:
                    continue
                
                # Convert published_at string to datetime
                published_at = datetime.fromisoformat(article_data.get('publishedAt', '').replace('Z', '+00:00'))
                
                # Create Article object
                article = Article(
                    id=article_id,
                    title=article_data.get('title', ''),
                    description=article_data.get('description'),
                    content=article_data.get('content'),
                    url=article_data.get('url'),
                    source_id=article_data.get('source', {}).get('id'),
                    source_name=article_data.get('source', {}).get('name', 'Unknown'),
                    author=article_data.get('author'),
                    published_at=published_at,
                    url_to_image=article_data.get('urlToImage'),
                    raw_data=article_data
                )
                articles.append(article)
            except Exception as e:
                self.logger.error(f"Error processing article: {e}")
                continue
        
        self.logger.info(f"Retrieved {len(articles)} articles")
        return articles
    
    def get_top_headlines(
        self,
        category: str = 'politics',
        country: str = 'us',
        page_size: int = 100,
        page: int = 1
    ) -> List[Article]:
        """
        Get top headlines in a specific category and country.
        
        Args:
            category: News category (default: 'politics')
            country: Country code (default: 'us')
            page_size: Number of articles per page (max 100)
            page: Page number
            
        Returns:
            List of Article objects
        """
        self.logger.info(f"Getting top headlines in {category} for {country}")
        
        try:
            response = self.client.get_top_headlines(
                category=category,
                country=country,
                page_size=page_size,
                page=page
            )
        except Exception as e:
            self.logger.error(f"Error fetching top headlines: {e}")
            return []
        
        if not response or 'articles' not in response or not response['articles']:
            self.logger.warning(f"No headlines found for category: {category} in country: {country}")
            return []
        
        # Convert to Article objects (same as above)
        articles = []
        for article_data in response['articles']:
            try:
                # Generate a unique ID for the article (using URL hash)
                import hashlib
                url = article_data.get('url', '')
                article_id = hashlib.md5(url.encode()).hexdigest() if url else None
                
                if not article_id:
                    continue
                
                # Convert published_at string to datetime
                published_at = datetime.fromisoformat(article_data.get('publishedAt', '').replace('Z', '+00:00'))
                
                # Create Article object
                article = Article(
                    id=article_id,
                    title=article_data.get('title', ''),
                    description=article_data.get('description'),
                    content=article_data.get('content'),
                    url=article_data.get('url'),
                    source_id=article_data.get('source', {}).get('id'),
                    source_name=article_data.get('source', {}).get('name', 'Unknown'),
                    author=article_data.get('author'),
                    published_at=published_at,
                    url_to_image=article_data.get('urlToImage'),
                    raw_data=article_data
                )
                articles.append(article)
            except Exception as e:
                self.logger.error(f"Error processing article: {e}")
                continue
        
        self.logger.info(f"Retrieved {len(articles)} headlines")
        return articles