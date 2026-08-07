from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Shared user fields used by user-facing request and response schemas."""

    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., max_length=255)


class UserCreate(UserBase):
    """Payload for creating a new user account."""

    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(default="candidate", min_length=1, max_length=20)

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    """Payload for authenticating an existing user."""

    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(UserBase):
    """Public user representation returned by API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    created_at: datetime
