"""
Pydantic schemas package.
"""

from .common import ErrorResponse, SuccessResponse
from .job import JobBase, JobCreate, JobResponse
from .resume import ResumeBase, ResumeCreate, ResumeResponse
from .user import UserBase, UserCreate, UserLogin, UserResponse

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",

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