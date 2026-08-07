from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import verify_access_token
from app.database.database import SessionLocal
from app.models.user import User
from app.schemas.auth import TokenData
from app.services.user_service import get_user_by_id


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for each request.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Resolve the authenticated user from a Bearer token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_access_token(token)

    if payload is None:
        raise credentials_exception

    try:
        user_id = int(payload["sub"]) if payload.get("sub") is not None else None
    except (TypeError, ValueError):
        raise credentials_exception

    token_data = TokenData(
        user_id=user_id,
        email=payload.get("email"),
        role=payload.get("role"),
    )

    if token_data.user_id is None:
        raise credentials_exception

    user = get_user_by_id(db, token_data.user_id)

    if user is None:
        raise credentials_exception

    return user


class RequireRole:
    """
    FastAPI dependency that allows only users with one of the configured roles.
    """

    def __init__(self, *allowed_roles: str) -> None:
        self.allowed_roles = set(allowed_roles)

    def __call__(
        self,
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user
