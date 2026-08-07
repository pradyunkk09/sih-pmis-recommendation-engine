from pydantic import BaseModel


class Token(BaseModel):
    """JWT response returned after successful authentication."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """User identity extracted from a verified JWT."""

    user_id: int | None = None
    email: str | None = None
    role: str | None = None
