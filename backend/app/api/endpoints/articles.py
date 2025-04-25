from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date, datetime
import io
import csv
import time
import re

from app.db.session import get_db
from app.models import Article, PoliticalStance
from app.models.database import ArticleModel, ClassificationModel
from app.services.news_client import NewsClient
from app.services.article_service import ArticleService

router = APIRouter()

def parse_datetime(date_str: str) -> datetime:
    """
    Parse different datetime formats and return a datetime object.
    """
    if not date_str:
        return datetime.utcnow()
    
    # Try different formats
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",  # Standard ISO format with Z
        "%Y-%m-%dT%H:%M:%S.%fZ", # ISO format with milliseconds and Z
        "%Y-%m-%dT%H:%M:%S", # ISO format without Z
        "%Y-%m-%dT%H:%M:%S.%f", # ISO format with milliseconds without Z
        "%Y-%m-%d %H:%M:%S", # Simple format
        "%Y-%m-%d", # Just date
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # If all formats fail, try to parse ISO format with timezone offset
    try:
        # Replace Z with +00:00 (UTC) if present
        if date_str.endswith('Z'):
            date_str = date_str[:-1] + '+00:00'
        
        # Parse ISO format with timezone info
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass
    
    # If all parsing attempts fail, return current time
    print(f"Could not parse datetime: {date_str}, using current time")
    return datetime.utcnow()

@router.get("/", response_model=List[Article])
async def get_articles(
    db: Session = Depends(get_db),
    stance: Optional[PoliticalStance] = Query(None, description="Filter articles by political stance"),
    search: Optional[str] = Query(None, description="Search query to filter articles"),
    source: Optional[str] = Query(None, description="Filter by news source"),
    start_date: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
) -> List[Article]:
    """
    Get articles with optional filtering by various criteria.
    """
    try:
        # Start with base query
        query = db.query(ArticleModel)
        
        # Apply filters
        if stance:
            query = query.join(ClassificationModel).filter(ClassificationModel.stance == stance)
            
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    ArticleModel.title.ilike(search_term),
                    ArticleModel.description.ilike(search_term),
                    ArticleModel.content.ilike(search_term)
                )
            )
            
        if source:
            query = query.filter(ArticleModel.source_name.ilike(f"%{source}%"))
            
        if start_date:
            query = query.filter(ArticleModel.published_at >= start_date)
            
        if end_date:
            query = query.filter(ArticleModel.published_at <= end_date)
        
        # Apply pagination
        articles = query.offset(skip).limit(limit).all()
        
        return articles
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving articles: {str(e)}"
        )

@router.post("/save")
async def save_articles(
    articles: List[Article],
    db: Session = Depends(get_db)
) -> dict:
    """
    Save articles to the database.
    """
    try:
        saved_count = 0
        skipped_count = 0
        errors = []
        
        print(f"Received {len(articles)} articles to save")
        
        for i, article in enumerate(articles):
            try:
                # Log the article being processed
                print(f"Processing article {i+1}/{len(articles)}: '{article.title}'")
                
                # Ensure URL is properly formatted
                article_url = str(article.url)
                if not article_url.startswith(("http://", "https://")):
                    article_url = f"https://{article_url}"
                    article.url = article_url
                
                print(f"URL: {article_url}")
                
                # Check if article already exists by URL
                existing_article = db.query(ArticleModel).filter(ArticleModel.url == article_url).first()
                
                if existing_article:
                    print(f"Article with URL {article_url} already exists")
                    skipped_count += 1
                    continue
                
                # Check if article already exists by title (as a fallback)
                existing_by_title = db.query(ArticleModel).filter(ArticleModel.title == article.title).first()
                if existing_by_title:
                    print(f"Found existing article with same title: {existing_by_title.title}")
                    skipped_count += 1
                    continue
                
                # Generate a unique ID if not present
                article_id = article.id if hasattr(article, 'id') and article.id else f"article_{saved_count}_{int(time.time())}"
                print(f"Using ID: {article_id}")
                
                # Ensure published_at is a valid datetime
                try:
                    published_at = parse_datetime(article.published_at)
                    print(f"Parsed date: {published_at}")
                except Exception as e:
                    print(f"Error parsing date '{article.published_at}': {str(e)}")
                    published_at = datetime.utcnow()
                    print(f"Using current time instead: {published_at}")
                
                # Convert Pydantic model to SQLAlchemy model
                db_article = ArticleModel(
                    id=article_id,
                    title=article.title,
                    description=article.description,
                    content=article.content if hasattr(article, 'content') else None,
                    url=article_url,
                    source_id=article.source_id if hasattr(article, 'source_id') else None,
                    source_name=article.source_name,
                    author=article.author if hasattr(article, 'author') else None,
                    published_at=published_at,
                    url_to_image=str(article.url_to_image) if hasattr(article, 'url_to_image') and article.url_to_image else None,
                    raw_data=article.raw_data if hasattr(article, 'raw_data') else {}
                )
                db.add(db_article)
                saved_count += 1
                print(f"Article '{article.title}' scheduled for saving")
            except Exception as e:
                error_msg = f"Error with article '{article.title}': {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                # Don't fail completely on a single article error
                continue
        
        if saved_count > 0:
            print(f"Committing {saved_count} articles to database")
            db.commit()
            
            # Double-check the articles were saved
            for article in articles:
                article_title = article.title
                found = db.query(ArticleModel).filter(ArticleModel.title == article_title).first()
                if found:
                    print(f"Confirmed article saved: {article_title}")
                else:
                    print(f"WARNING: Could not confirm article was saved: {article_title}")
        else:
            print("No articles to commit")
        
        result = {
            "message": f"Successfully saved {saved_count} articles to the database"
        }
        
        if skipped_count > 0:
            result["skipped"] = skipped_count
            result["message"] += f" (skipped {skipped_count} duplicates)"
            
        if errors:
            result["errors"] = errors
            
        return result
        
    except Exception as e:
        db.rollback()
        error_msg = f"Error saving articles: {str(e)}"
        print(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@router.get("/export")
async def export_articles(
    db: Session = Depends(get_db),
    stance: Optional[PoliticalStance] = Query(None, description="Filter articles by political stance"),
    search: Optional[str] = Query(None, description="Search query to filter articles"),
    source: Optional[str] = Query(None, description="Filter by news source"),
    start_date: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)")
):
    """
    Export articles to CSV with optional filtering.
    """
    try:
        # Build query
        query = db.query(ArticleModel)
        
        if stance:
            query = query.join(ClassificationModel).filter(ClassificationModel.stance == stance)
            
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    ArticleModel.title.ilike(search_term),
                    ArticleModel.description.ilike(search_term),
                    ArticleModel.content.ilike(search_term)
                )
            )
            
        if source:
            query = query.filter(ArticleModel.source_name.ilike(f"%{source}%"))
            
        if start_date:
            query = query.filter(ArticleModel.published_at >= start_date)
            
        if end_date:
            query = query.filter(ArticleModel.published_at <= end_date)
        
        # Get articles
        articles = query.all()
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "ID", "Title", "Description", "Source", "Author",
            "Published At", "URL", "Political Stance", "Confidence"
        ])
        
        # Write data
        for article in articles:
            stance = article.classification.stance if article.classification else "Unknown"
            confidence = article.classification.confidence if article.classification else 0.0
            
            writer.writerow([
                article.id,
                article.title,
                article.description or "",
                article.source_name,
                article.author or "",
                article.published_at.isoformat(),
                str(article.url),
                stance,
                confidence
            ])
        
        # Create response
        content = output.getvalue()
        output.close()
        
        return Response(
            content=content,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=articles.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting articles: {str(e)}"
        )

@router.post("/collect")
async def collect_articles(
    topic: Optional[str] = Query(None, description="Topic to collect articles about"),
    category: Optional[str] = Query(None, description="Category for top headlines"),
    language: str = Query("en", description="Language code (e.g., 'en' for English, 'es' for Spanish)"),
    days_back: int = Query(7, description="Number of days to look back for articles"),
    page_size: int = Query(100, description="Number of articles per page"),
    page: int = Query(1, description="Page number"),
    country: Optional[str] = Query(None, description="Country code for top headlines (e.g., 'us')"),
    db: Session = Depends(get_db)
) -> List[Article]:
    """
    Collect articles using either topic search or top headlines.
    """
    # Initialize NewsClient
    news_client = NewsClient()
    
    # Get articles based on provided parameters
    if topic:
        # Use get_articles_by_topic
        articles = news_client.get_articles_by_topic(
            topic=topic,
            language=language,
            days_back=days_back,
            page_size=page_size,
            page=page
        )
    elif category:
        # Use get_top_headlines
        articles = news_client.get_top_headlines(
            category=category,
            country=country,
            page_size=page_size,
            page=page
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Either 'topic' or 'category' must be provided"
        )
    
    return articles 

@router.get("/saved", response_model=List[Article])
async def get_saved_articles(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of articles to return"),
    offset: int = Query(0, ge=0, description="Number of articles to skip")
) -> List[Article]:
    """
    Get articles that have been saved to the database.
    """
    try:
        # Get saved articles with pagination, ordered by published_at descending
        articles = db.query(ArticleModel).order_by(ArticleModel.published_at.desc()).offset(offset).limit(limit).all()
        
        return articles
        
    except Exception as e:
        error_msg = f"Error retrieving saved articles: {str(e)}"
        print(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@router.delete("/clear")
async def clear_database(
    db: Session = Depends(get_db)
) -> dict:
    """
    Clear all saved articles from the database.
    """
    try:
        # Count articles before deletion
        article_count = db.query(ArticleModel).count()
        
        # Delete all articles
        db.query(ArticleModel).delete()
        db.commit()
        
        return {
            "message": f"Successfully deleted {article_count} articles from the database"
        }
        
    except Exception as e:
        db.rollback()
        error_msg = f"Error clearing database: {str(e)}"
        print(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        ) 