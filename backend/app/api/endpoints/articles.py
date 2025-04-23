from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Article, PoliticalStance
from app.models.database import ArticleModel, ClassificationModel
from app.services.news_client import NewsClient
from app.services.article_service import ArticleService

router = APIRouter()

@router.get("/", response_model=List[Article])
async def get_articles(
    db: Session = Depends(get_db),
    stance: Optional[PoliticalStance] = Query(None, description="Filter articles by political stance"),
    search: Optional[str] = Query(None, description="Search query to filter articles"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
) -> List[Article]:
    """
    Get articles with optional filtering by political stance and search query.
    
    Args:
        db: Database session
        stance: Optional political stance to filter by
        search: Optional search query to filter by
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return
        
    Returns:
        List of Article objects matching the criteria
        
    Raises:
        HTTPException: If database query fails
    """
    try:
        query = db.query(ArticleModel)
        
        # Apply stance filter if provided
        if stance:
            query = query.join(ClassificationModel).filter(
                ClassificationModel.stance == stance
            )
        
        # Apply search filter if provided
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (ArticleModel.title.ilike(search_pattern)) |
                (ArticleModel.description.ilike(search_pattern))
            )
        
        # Apply pagination
        articles = query.offset(skip).limit(limit).all()
        
        # Convert SQLAlchemy models to Pydantic models
        return [Article.from_orm(article) for article in articles]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching articles: {str(e)}"
        )

@router.get("/export")
async def export_articles(
    db: Session = Depends(get_db),
    stance: Optional[PoliticalStance] = Query(None, description="Filter articles by political stance"),
    search: Optional[str] = Query(None, description="Search query to filter articles")
):
    """
    Export articles to CSV with optional filtering.
    
    Args:
        db: Database session
        stance: Optional political stance to filter by
        search: Optional search query to filter by
        
    Returns:
        CSV file with article data
        
    Raises:
        HTTPException: If export fails
    """
    try:
        # This is a placeholder for Day 1
        # In Day 2, we'll implement the actual CSV export
        return {"message": "CSV export not yet implemented"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting articles: {str(e)}"
        )

@router.post("/collect")
async def collect_articles(
    topic: str = Query(..., description="Topic to collect articles about"),
    db: Session = Depends(get_db)
) -> dict:
    """
    Collect articles about a specific topic and save them to the database.
    """
    # Initialize NewsClient
    news_client = NewsClient()
    
    # Get articles from NewsAPI
    articles = news_client.get_articles_by_topic(topic)
    
    # Save articles to database
    saved_articles = ArticleService.save_articles(db, articles)
    
    return {
        "message": f"Successfully collected and saved {len(saved_articles)} articles",
        "topic": topic
    } 