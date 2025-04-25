from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import datetime

# Get current path
current_path = os.getcwd()
print(f"Current path: {current_path}")

# We need to import from the right location
import sys
backend_path = os.path.join(current_path, "backend")
sys.path.append(backend_path)

from app.models.database import Base, ArticleModel

# Create engine - get current username for db access
username = os.getenv('USER')
db_url = f'postgresql://{username}@localhost:5432/political_content'
print(f"Using database URL: {db_url}")

try:
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print("Successfully connected to database and created tables")

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create test article
    test_article = ArticleModel(
        id='test_article_1',
        title='Test Article',
        description='This is a test article',
        url='https://example.com/test',
        source_name='Test Source',
        published_at=datetime.datetime.now(),
        content='Test content'
    )

    # Add to session and commit
    session.add(test_article)
    session.commit()
    print("Test article added to database")

    # Verify it's there
    article = session.query(ArticleModel).filter_by(id='test_article_1').first()
    print(f'Article retrieved: {article.id} - {article.title}')
    
    # Count total articles
    count = session.query(ArticleModel).count()
    print(f"Total articles in database: {count}")
    
except Exception as e:
    print(f"Error: {str(e)}") 