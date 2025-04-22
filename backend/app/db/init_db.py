import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.db.session import engine
from app.models import Base

logger = logging.getLogger(__name__)

def init_db(db: Optional[Session] = None) -> None:
    """Initialize database tables.
    
    Args:
        db: Optional database session. If not provided, a new session will be created.
    """
    try:
        logger.info("Creating database tables")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise 