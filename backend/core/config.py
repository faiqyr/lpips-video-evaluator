from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LPIPS Video Evaluation Platform"
    API_V1_STR: str = "/api/v1"
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./lpips.db"
    
    # Storage
    UPLOAD_DIR: str = "uploads"
    FRAME_DIR: str = "frames"

settings = Settings()
