from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import datetime
import json
import uuid

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
    
    # Create multiple test articles to mimic the save functionality
    test_articles = []
    for i in range(1, 6):
        article_id = str(uuid.uuid4())
        test_article = ArticleModel(
            id=article_id,
            title=f'Test Article {i}',
            description=f'This is test article number {i}',
            url=f'https://example.com/test{i}',
            source_name=f'Test Source {i}',
            published_at=datetime.datetime.now(),
            content=f'Test content for article {i}',
            raw_data=json.dumps({"test": True, "number": i})
        )
        session.add(test_article)
        test_articles.append(article_id)
    
    # Commit the changes
    session.commit()
    print(f"Added {len(test_articles)} test articles to database")

    # Verify they're there
    for article_id in test_articles:
        article = session.query(ArticleModel).filter_by(id=article_id).first()
        print(f'Article retrieved: {article.id} - {article.title}')
    
    # Count total articles
    count = session.query(ArticleModel).count()
    print(f"Total articles in database: {count}")
    
except Exception as e:
    print(f"Error: {str(e)}") 