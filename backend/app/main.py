from fastapi import FastAPI #core application class 
from fastapi.middleware.cors import CORSMiddleware #middleware for cross-origin resource sharing

from app.core.config import settings
from app.db.init_db import init_db
from app.api import api_router
"""
Entry point of the app -> main script for running the FastAPI application
Data flow: User Command → collect_articles.py → NewsClient → NewsAPI → Article Model → JSON Output
NewsClient (backend/app/services/news_client.py):
    - Initializes the NewsAPI client with the API key
    - Defines the get_articles_by_topic method
    - Uses the NewsAPI client to get articles by topic
    - Returns a list of Article objects (converts raw API response to Article model JSON)

Data Models
Article (backend/app/models/article.py):
    -  Pydantic model for article data validation
    - Fields include: id, title, description, content, url, source info, etc.
    - Includes raw_data for storing original API response

Configuration
settings (backend/app/core/config.py):
    - Manages environment variables and configuration
    - Currently handles NewsAPI key

run:
    uvicorn main:app --reload
Visit http://127.0.0.1:8000/docs for Swagger
Visit http://127.0.0.1:8000/redoc for ReDoc
"""

# Create FastAPI application
app = FastAPI(
    title="News Pulse",
    description="An application that analyzes political content from news articles",
    version="0.1.0"
)

# Add CORS middleware
# This allows the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Initialize database tables on startup
@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
async def root(): #async for concurrent operations -> FastAPI runs it in its event loop
    return {"message": "Welcome to Political Content Analyzer API"} #returns any serializable python object




