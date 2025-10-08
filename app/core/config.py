from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "AI Resume Matcher"
    DEBUG: bool = True
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    

    class Config:
        env_file = ".env"

settings = Settings()
