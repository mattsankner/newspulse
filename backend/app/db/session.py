from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create SQLAlchemy engine
# The engine manages the connection pool and database connections
engine = create_engine(
    settings.DATABASE_URL,
    # Enable connection pooling
    pool_pre_ping=True,
    # Set pool size
    pool_size=5,
    # Set max overflow
    max_overflow=10
)

# Create session factory
# This is used to create new database sessions
SessionLocal = sessionmaker(
    autocommit=False,  # Don't automatically commit changes
    autoflush=False,   # Don't automatically flush changes
    bind=engine        # Use our engine for connections
)

# Dependency to get database session
# This is used by FastAPI to manage database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 