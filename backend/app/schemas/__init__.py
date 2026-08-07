"""
Pydantic schemas package.
"""

from .common import ErrorResponse, SuccessResponse
from .auth import Token, TokenData
from .job import JobBase, JobCreate, JobResponse
from .resume import ResumeBase, ResumeCreate, ResumeResponse
from .user import UserBase, UserCreate, UserLogin, UserResponse

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",

    # Authentication
    "Token",
    "TokenData",

    # Resume
    "ResumeBase",
    "ResumeCreate",
    "ResumeResponse",

    # Job
    "JobBase",
    "JobCreate",
    "JobResponse",

    # Common
    "SuccessResponse",
    "ErrorResponse",
]
