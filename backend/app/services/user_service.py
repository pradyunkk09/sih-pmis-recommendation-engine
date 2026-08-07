from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user in the database.
    """
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password=user_data.password,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Retrieve a user by their ID.

    Args:
        db: Active SQLAlchemy session.
        user_id: Primary key of the user.

    Returns:
        User object if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user by their email address.

    Args:
        db: Active SQLAlchemy session.
        email: User email.

    Returns:
        User object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session) -> list[User]:
    """
    Retrieve all users.

    Args:
        db: Active SQLAlchemy session.

    Returns:
        List of User objects.
    """
    return db.query(User).all()