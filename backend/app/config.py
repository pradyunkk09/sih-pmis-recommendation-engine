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


# Shared settings instance for clean imports across the backend:
# from app.config import settings
settings = Settings()

# Direct module-level export for components that only need the database URL.
DATABASE_URL = settings.DATABASE_URL
