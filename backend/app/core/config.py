from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_NAME: str = "Document Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001", "*"]
    UPLOAD_FOLDER: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "uploads")
    PROCESSED_FOLDER: str = "/Users/olawalebadekale/ai-document-platform/data/processed"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    DATABASE_URL: str = "sqlite:///./doc_intelligence.db"

settings = Settings()
