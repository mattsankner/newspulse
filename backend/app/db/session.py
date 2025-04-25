from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings

def get_database_url():
    """Get database URL with appropriate user configuration."""
    # Get the current user
    current_user = os.getenv('USER') or os.getenv('USERNAME')
    
    # Default database URL template
    db_url = f"postgresql://{current_user}@localhost:5432/political_content"
    
    # If DATABASE_URL is set in environment, use it
    if os.getenv('DATABASE_URL'):
        db_url = os.getenv('DATABASE_URL')
    
    print(f"Using database URL: {db_url}")
    return db_url

# Create SQLAlchemy engine with error handling
try:
    db_url = get_database_url().replace('postgresql://', 'postgresql+psycopg://')
    print(f"Creating engine with URL: {db_url}")
    
    engine = create_engine(
        db_url,
        # Enable connection pooling
        pool_pre_ping=True,
        # Set pool size
        pool_size=5,
        # Set max overflow
        max_overflow=10
    )
    
    # Test the connection
    with engine.connect() as conn:
        print("✅ Database connection successful")
        
except SQLAlchemyError as e:
    print(f"❌ Database connection error: {str(e)}")
    print("\nTo fix this, ensure:")
    print("1. PostgreSQL is installed and running")
    print("2. The database 'political_content' exists")
    print("3. Your user has access to the database")
    print("\nYou can create the database with:")
    print("createdb political_content")
    raise

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
    """Get database session with error handling."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"❌ Database error during request: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

# Create or update .env file
#below caused error sh: backend/.env: No such file or directory when running run.sh
#os.system("echo \"DATABASE_URL=postgresql://$(whoami)@localhost:5432/political_content\" > backend/.env")
os.system(f"echo \"DATABASE_URL=postgresql://$(whoami)@localhost:5432/political_content\" > {os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.env'))}")