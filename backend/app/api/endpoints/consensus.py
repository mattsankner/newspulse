from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.models.stance import Consensus, PoliticalStance
from app.models.database import ArticleModel, ConsensusModel

router = APIRouter()

@router.get("/", response_model=List[Consensus])
async def get_consensus(
    topic: str = Query(..., description="Topic to find consensus about"),
    db: Session = Depends(get_db),
    days_back: int = Query(7, description="Number of days to look back for articles")
) -> List[Consensus]:
    """
    Find consensus points among different political viewpoints for a given topic.
    """
    try:
        # Get articles about the topic
        articles = db.query(ArticleModel).filter(
            ArticleModel.published_at >= datetime.utcnow() - timedelta(days=days_back)
        ).all()
        
        # Group articles by stance
        left_articles = [a for a in articles if a.classification and a.classification.stance == PoliticalStance.LEFT]
        center_articles = [a for a in articles if a.classification and a.classification.stance == PoliticalStance.CENTER]
        right_articles = [a for a in articles if a.classification and a.classification.stance == PoliticalStance.RIGHT]
        
        # Extract key points from each stance
        left_points = extract_key_points(left_articles)
        center_points = extract_key_points(center_articles)
        right_points = extract_key_points(right_articles)
        
        # Find common ground
        common_ground = find_common_ground(left_points, center_points, right_points)
        
        # Create consensus object
        consensus = Consensus(
            id=str(uuid.uuid4()),
            topic=topic,
            summary=generate_summary(left_points, center_points, right_points, common_ground),
            left_points=left_points,
            center_points=center_points,
            right_points=right_points,
            common_ground=common_ground
        )
        
        # Save to database
        db_consensus = ConsensusModel(
            id=consensus.id,
            topic=consensus.topic,
            summary=consensus.summary,
            left_points=consensus.left_points,
            center_points=consensus.center_points,
            right_points=consensus.right_points,
            common_ground=consensus.common_ground
        )
        db.add(db_consensus)
        db.commit()
        
        return [consensus]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding consensus: {str(e)}"
        )

def extract_key_points(articles: List[ArticleModel]) -> List[str]:
    """Extract key points from articles."""
    # Simple implementation - extract sentences containing key terms
    key_points = []
    for article in articles:
        if article.content:
            sentences = article.content.split('.')
            key_points.extend([s.strip() for s in sentences if len(s.strip()) > 50])
    return key_points[:10]  # Limit to top 10 points

def find_common_ground(left_points: List[str], center_points: List[str], right_points: List[str]) -> List[str]:
    """Find common ground among different viewpoints."""
    # Simple implementation - find overlapping terms
    all_points = left_points + center_points + right_points
    word_counts = {}
    for point in all_points:
        words = point.lower().split()
        for word in words:
            if len(word) > 4:  # Only consider words longer than 4 characters
                word_counts[word] = word_counts.get(word, 0) + 1
    
    # Find words that appear in at least two stances
    common_words = [word for word, count in word_counts.items() if count >= 2]
    
    # Find points containing common words
    common_ground = []
    for point in all_points:
        if any(word in point.lower() for word in common_words):
            common_ground.append(point)
    
    return common_ground[:5]  # Limit to top 5 common points

def generate_summary(left_points: List[str], center_points: List[str], right_points: List[str], common_ground: List[str]) -> str:
    """Generate a summary of the consensus."""
    summary = f"Analysis of {len(left_points)} left-leaning, {len(center_points)} center, and {len(right_points)} right-leaning articles found:\n\n"
    
    if common_ground:
        summary += "Common ground:\n"
        for point in common_ground:
            summary += f"- {point}\n"
    
    return summary 