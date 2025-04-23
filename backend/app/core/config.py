import os
from pydantic_settings import BaseSettings #Pydantic base settings class designed for environment variables
from dotenv import load_dotenv #loads environment variables from .env file

"""Keeps configuration (API versions, credentials, URL's, CORS settings, etc.) out of business logic"""

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Political Content Analyzer"
    
    # News API Keys
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{os.getenv('USER', os.getenv('USERNAME', 'postgres'))}@localhost:5432/political_content"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:4200"] #automatic type conversion to real python list

settings = Settings()