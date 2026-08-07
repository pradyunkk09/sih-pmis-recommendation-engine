from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.database.base import Base


# The engine manages low-level database connections for the application.
# SQLite needs check_same_thread=False because FastAPI can handle requests across
# different threads, while SQLite restricts connections to their creating thread
# by default.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal creates short-lived database sessions. Each request should receive
# its own session so transactions and connection cleanup stay isolated.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # Yield a database session to FastAPI dependencies and always close it after
    # the request finishes, even if endpoint code raises an exception.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
