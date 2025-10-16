from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    # test
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    API_PRSSSSEFIX: str = os.getenv("API_PREFIX", "/api")
    
    # Database Configuration
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "app/data/vulnerabilities.db")
    DATABASE_PATH_TEST: str = os.getenv("DATABASE_PATH", "app/data/vulnerabilities.db")
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")
    AZURE_OPENAI_COMPLETIONS_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_COMPLETIONS_DEPLOYMENT")
    
    # Vector Database Configuration
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "app/data/vector_db")
    
    # Scraper Configuration
    SNYK_BASE_URL: str = os.getenv("SNYK_BASE_URL", "https://security.snyk.io/vuln/pip/")
    SCRAPER_PAGES_TO_FETCH: int = int(os.getenv("SCRAPER_PAGES_TO_FETCH", 10))
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Create settings instance
settings = Settings()
