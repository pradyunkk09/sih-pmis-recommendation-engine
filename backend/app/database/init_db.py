from app.database.database import Base, engine
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User


def init_db() -> None:
    """Create database tables for all registered SQLAlchemy models."""

    # Model imports above ensure SQLAlchemy registers every table in metadata.
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
