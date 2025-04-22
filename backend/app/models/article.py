from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, HttpUrl
"""
These "models" are simply typed classes that define the shape of data coming into and out of the API.
They power validation, serialization, documentation, and (with orm_mode) easy database integration.
"""

#These are data schemas defined with Pydantic's BaseModel.
class Article(BaseModel):
    """Model representing a news article."""
    id: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: HttpUrl
    source_id: Optional[str] = None
    source_name: str
    author: Optional[str] = None
    published_at: datetime
    url_to_image: Optional[HttpUrl] = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        from_attributes = True
        #allow ORM mode for SQLAlchemy
        #allows FastAPI to convert Pydantic models to SQLAlchemy models
        #allow pydantic to read attributes off ORM objects (e.g. tweet.id, tweet.text) without needing
        #raw dicts. That way you can return a SQLAlchemy TweetDBModel direclty in a route and have FastAPI
        #serialize it via your Pydantic Tweet schema
