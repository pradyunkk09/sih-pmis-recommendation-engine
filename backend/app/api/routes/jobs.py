from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.job import (
    JobCreate,
    JobResponse,
    JobUpdate,
)
from app.services.job_service import (
    create_job,
    delete_job,
    get_all_jobs,
    get_job_by_id,
    update_job,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "/",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    return create_job(db, job)


@router.get(
    "/",
    response_model=list[JobResponse],
)
def read_all_jobs(
    db: Session = Depends(get_db),
):
    return get_all_jobs(db)


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def read_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def edit_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
):
    job = update_job(
        db,
        job_id,
        job_data,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_job(
        db,
        job_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )