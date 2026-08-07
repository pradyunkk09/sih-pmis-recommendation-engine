from sqlalchemy.orm import Session

from app.auth import verify_password
from app.models.user import User
from app.services.user_service import get_user_by_email


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Return the user when the email exists and the password is valid.
    """
    user = get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
