from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "BLR Vendor-Event Discovery"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey" # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    MONGO_URL: str = "mongodb://mongo:27017"
    MONGO_DB_NAME: str = "blr_geo_events"
    
    class Config:
        env_file = ".env"

settings = Settings()
