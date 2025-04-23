from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class PoliticalStance(str, Enum):
    """Enum representing political stance."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    UNKNOWN = "unknown"

class Classification(BaseModel):
    """Model representing political stance classification."""
    article_id: str
    stance: PoliticalStance
    confidence: float
    
    class Config:
        from_attributes = True

class Consensus(BaseModel):
    """Model representing identified consensus between political viewpoints."""
    id: str
    topic: str
    summary: str
    left_points: list[str] = []
    center_points: list[str] = []
    right_points: list[str] = []
    common_ground: list[str] = []
    
    class Config:
        from_attributes = True