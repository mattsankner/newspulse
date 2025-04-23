from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.stance import Classification, PoliticalStance
from app.models.database import ArticleModel, ClassificationModel

router = APIRouter()

@router.post("/", response_model=List[Classification])
async def analyze_articles(
    topic: Optional[str] = Query(None, description="Topic to analyze articles about"),
    days_back: int = Query(7, description="Number of days to look back for articles"),
    db: Session = Depends(get_db)
) -> List[Classification]:
    """
    Analyze political alignment of articles.
    """
    try:
        # Get articles to analyze
        query = db.query(ArticleModel)
        if topic:
            query = query.filter(ArticleModel.title.ilike(f"%{topic}%"))
        query = query.filter(
            ArticleModel.published_at >= datetime.utcnow() - timedelta(days=days_back)
        )
        articles = query.all()
        
        # Analyze each article
        classifications = []
        for article in articles:
            # Skip if already classified
            if article.classification:
                classifications.append(article.classification)
                continue
                
            # Analyze article content
            stance = analyze_article(article)
            
            # Create classification
            classification = Classification(
                article_id=article.id,
                stance=stance,
                confidence=0.8  # Placeholder confidence score
            )
            
            # Save to database
            db_classification = ClassificationModel(
                article_id=classification.article_id,
                stance=classification.stance,
                confidence=classification.confidence
            )
            db.add(db_classification)
            classifications.append(classification)
            
        db.commit()
        return classifications
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing articles: {str(e)}"
        )

def analyze_article(article: ArticleModel) -> PoliticalStance:
    """Analyze an article's political stance."""
    # Simple implementation using keyword matching
    left_keywords = ["democrat", "progressive", "liberal", "left", "socialist"]
    right_keywords = ["republican", "conservative", "right", "trump", "gop"]
    
    content = (article.title + " " + (article.description or "") + " " + (article.content or "")).lower()
    
    left_count = sum(1 for word in left_keywords if word in content)
    right_count = sum(1 for word in right_keywords if word in content)
    
    if left_count > right_count:
        return PoliticalStance.LEFT
    elif right_count > left_count:
        return PoliticalStance.RIGHT
    else:
        return PoliticalStance.CENTER 