from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResumeBase(BaseModel):
    """Shared resume fields accepted by resume-related API operations."""

    filename: str = Field(..., min_length=1, max_length=255)


class ResumeCreate(ResumeBase):
    """Payload for creating a resume record after a file upload."""

    file_path: str = Field(..., min_length=1, max_length=500)
    parsed_text: str | None = None


class ResumeResponse(ResumeBase):
    """Public resume representation returned by API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    file_path: str
    parsed_text: str | None
    upload_date: datetime
