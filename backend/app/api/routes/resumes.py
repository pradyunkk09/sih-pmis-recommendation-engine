from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.resume import (
    ResumeCreate,
    ResumeResponse,
    ResumeUpdate,
)
from app.services.resume_service import (
    create_resume,
    delete_resume,
    get_resume_by_id,
    get_resumes_by_user_id,
    update_resume,
)

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "/",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_resume(
    resume: ResumeCreate,
    db: Session = Depends(get_db),
):
    return create_resume(db, resume)


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def read_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    resume = get_resume_by_id(db, resume_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


@router.get(
    "/user/{user_id}",
    response_model=list[ResumeResponse],
)
def read_user_resumes(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_resumes_by_user_id(db, user_id)


@router.put(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def edit_resume(
    resume_id: int,
    resume_data: ResumeUpdate,
    db: Session = Depends(get_db),
):
    resume = update_resume(
        db,
        resume_id,
        resume_data,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_resume(
    resume_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_resume(
        db,
        resume_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )