# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Resume Matcher"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
