from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResumeBase(BaseModel):
    """Shared resume fields accepted by resume-related API operations."""

    filename: str = Field(..., min_length=1, max_length=255)

class ResumeCreate(ResumeBase):
    """Payload for creating a resume record after a file upload."""

    user_id: int

    file_path: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )

    parsed_text: str | None = None
    qualification: str | None = None
    skills: str | None = None
    district: str | None = None
    state: str | None = None
    profile_summary: str | None = None

class ResumeUpdate(BaseModel):
    filename: str | None = Field(default=None, min_length=1, max_length=255)
    file_path: str | None = Field(default=None, min_length=1, max_length=500)
    parsed_text: str | None = None
    qualification: str | None = None
    skills: str | None = None
    district: str | None = None
    state: str | None = None
    profile_summary: str | None = None
    model_config = ConfigDict(from_attributes=True)

class ResumeResponse(ResumeBase):
    """Public resume representation returned by API endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    file_path: str
    parsed_text: str | None
    upload_date: datetime
    qualification: str | None
    skills: str | None
    district: str | None
    state: str | None
    profile_summary: str | None