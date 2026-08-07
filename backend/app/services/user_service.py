from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db: Active SQLAlchemy session.
        user_data: Validated user creation schema.

    Returns:
        The newly created User ORM object.
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