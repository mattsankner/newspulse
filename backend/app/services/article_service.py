from typing import List
from sqlalchemy.orm import Session
from app.models.article import Article
from app.models.database import ArticleModel

class ArticleService:
    """Service for managing articles in the database."""
    
    @staticmethod
    def save_articles(db: Session, articles: List[Article]) -> List[ArticleModel]:
        """Save a list of articles to the database."""
        db_articles = []
        for article in articles:
            # Check if article already exists
            existing_article = db.query(ArticleModel).filter(ArticleModel.id == article.id).first()
            if existing_article:
                continue
                
            # Create new article model
            db_article = ArticleModel(
                id=article.id,
                title=article.title,
                description=article.description,
                content=article.content,
                url=str(article.url),
                source_id=article.source_id,
                source_name=article.source_name,
                author=article.author,
                published_at=article.published_at,
                raw_data=article.raw_data
            )
            
            db.add(db_article)
            db_articles.append(db_article)
            
        db.commit()
        return db_articles 