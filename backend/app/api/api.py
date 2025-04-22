from fastapi import APIRouter

from app.api.endpoints import articles

# Create main API router
api_router = APIRouter()

# Include article endpoints
api_router.include_router(
    articles.router,
    prefix="/articles",
    tags=["articles"]
) 