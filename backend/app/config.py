import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Keep configuration loading separate from application logic so routes,
# services, and database code can depend on explicit settings instead of
# reading environment variables directly. This makes the app easier to test,
# deploy, and update without changing business code.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    # Database connection string loaded from the environment.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )


# Shared settings instance for clean imports across the backend:
# from app.config import settings
settings = Settings()

# Direct module-level export for components that only need the database URL.
DATABASE_URL = settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
