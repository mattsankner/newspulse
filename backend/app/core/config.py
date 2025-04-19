import os
from pydantic import BaseSettings #Pydantic base settings class designed for environment variables
from dotenv import load_dotenv #loads environment variables from .env file

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Political Content Analyzer"
    
    # X (Twitter) API Keys
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET: str = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_BEARER_TOKEN: str = os.getenv("TWITTER_BEARER_TOKEN", "")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/political_content"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:4200"] #automatic type conversion to real python list

settings = Settings()