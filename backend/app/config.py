import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent.parent / '.env'

load_dotenv(dotenv_path=env_path)

class Settings:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    APP_NAME: str = os.getenv("APP_NAME", "People Counties API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")

    def __repr__(self):
        return f"Settings(DB_HOST={self.DB_HOST}, DB_NAME={self.DB_NAME}, DEBUG={self.DEBUG})"

settings = Settings()