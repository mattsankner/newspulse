"""
Database Models for News Pulse

This module defines the SQLAlchemy models for the PostgreSQL database, including:
- ArticleModel: Stores news articles with metadata and content
- ClassificationModel: Tracks political stance classifications for articles
- ConsensusModel: Stores identified consensus points between political viewpoints

The models use SQLAlchemy's declarative base and include:
- Column definitions with appropriate data types
- Relationships between models (e.g., article-classification)
- Table names and constraints
- Default values and nullable settings

These models serve as the foundation for:
- Storing article data from NewsAPI
- Tracking political stance classifications
- Maintaining consensus analysis results
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.models.stance import PoliticalStance


# Create declarative base class for models
Base = declarative_base()

class ArticleModel(Base):
    """SQLAlchemy model for news articles.

    Has a one-to-one relationship with ClassificationModel
    Includes fields for all article metadata and classification results
    Uses text type for large text fields (content, description, title)
    Uses string type for smaller text fields (id, url, source_id, source_name, author)
    Uses datetime type for timestamp fields (published_at)
    Uses enum type for political stance classification
    Uses JSON type for storing raw data from news API
    
    Attributes:
        id: Unique identifier for the article
        title: Article headline
        description: Article summary/description
        content: Full article content
        url: Original article URL
        source_id: ID of the news source
        source_name: Name of the news source
        author: Article author
        published_at: Publication timestamp
        url_to_image: URL to article's featured image
        raw_data: Raw JSON data from news API
    """
    __tablename__ = "articles"

    id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String, nullable=False)
    source_id = Column(String, nullable=True)
    source_name = Column(String, nullable=False)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=False)
    url_to_image = Column(String, nullable=True)
    raw_data = Column(JSON, nullable=True)
    
    # One-to-one relationship with classification
    classification = relationship("ClassificationModel", back_populates="article", uselist=False)

class ClassificationModel(Base):
    """SQLAlchemy model for political stance classifications.

    Links to articles via foreign key
    Uses enum type for political stance classification
    Uses float type for confidence score for classification
    Uses datetime type for timestamp of classification
    
    Attributes:
        id: Auto-incrementing primary key
        article_id: Foreign key to associated article
        stance: Political stance classification (left/center/right)
        confidence: Confidence score of the classification
    """
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String, ForeignKey("articles.id"), nullable=False)
    stance = Column(Enum(PoliticalStance), nullable=False)
    confidence = Column(Float, nullable=False)
    
    # Many-to-one relationship with article
    article = relationship("ArticleModel", back_populates="classification")

class ConsensusModel(Base):
    """SQLAlchemy model for consensus data.
    
    Attributes:
        id: Unique identifier for the consensus
        topic: Topic being analyzed
        summary: Summary of political consensus
        left_points: Key points from left-leaning sources
        center_points: Key points from center-leaning sources
        right_points: Key points from right-leaning sources
        common_ground: Points of agreement across stances
        created_at: Timestamp of consensus creation
    """
    __tablename__ = "consensus"

    id = Column(String, primary_key=True)
    topic = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    left_points = Column(JSON, default=list)
    center_points = Column(JSON, default=list)
    right_points = Column(JSON, default=list)
    common_ground = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow) 