"""
Pydantic schemas for the Job entity.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    """
    Base schema containing common job fields.
    """

    title: str = Field(..., min_length=2)
    company: str = Field(..., min_length=2)
    description: str = Field(..., min_length=10)
    skills_required: str = Field(..., min_length=2)
    location: str = Field(..., min_length=2)
    employment_type: str = Field(..., min_length=2)


class JobCreate(JobBase):
    """
    Schema used when creating a new job posting.
    """

    pass


class JobResponse(JobBase):
    """
    Schema returned when job information is sent to the client.
    """

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)