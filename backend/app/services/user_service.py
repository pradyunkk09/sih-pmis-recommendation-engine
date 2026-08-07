from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user in the database.
    """
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
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

def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
) -> User | None:
    """
    Update an existing user.

    Args:
        db: Active SQLAlchemy session.
        user_id: User ID.
        user_data: Fields to update.

    Returns:
        Updated User object, or None if not found.
    """

    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user from the database.

    Args:
        db: Active SQLAlchemy session.
        user_id: Primary key of the user.

    Returns:
        True if the user was deleted, False if the user was not found.
    """

    user = get_user_by_id(db, user_id)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True
