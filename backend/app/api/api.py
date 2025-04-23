from fastapi import APIRouter

from app.api.endpoints import articles, analyze, consensus

# Create main API router
api_router = APIRouter()

# Include article endpoints
api_router.include_router(
    articles.router,
    prefix="/articles",
    tags=["articles"]
)

# Include analysis endpoints
api_router.include_router(
    analyze.router,
    prefix="/analyze",
    tags=["analysis"]
)

# Include consensus endpoints
api_router.include_router(
    consensus.router,
    prefix="/consensus",
    tags=["consensus"]
) 