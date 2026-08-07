"""
Common reusable response schemas.
"""

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """
    Standard success response.
    """

    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    success: bool = False
    message: str