from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
"""
These “models” are simply typed classes that define the shape of data coming into and out of your API.
They power validation, serialization, documentation, and (with orm_mode) easy database integration.
"""
class Tweet(BaseModel):
    """Model representing a tweet from X (Twitter)."""
    id: str
    text: str
    author_id: str
    author_username: Optional[str] = None
    author_name: Optional[str] = None
    created_at: datetime
    retweet_count: int = 0
    like_count: int = 0
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        #allow ORM mode for SQLAlchemy
        #allows FastAPI to convert Pydantic models to SQLAlchemy models
        #allow pydantic to read attributes off ORM objects (e.g. tweet.id, tweet.text) without needing
        #raw dicts. That way you can return a SQLAlchemy TweetDBModel direclty in a route and have FastAPI
        #serialize it via your Pydantic Tweet schema
        orm_mode = True