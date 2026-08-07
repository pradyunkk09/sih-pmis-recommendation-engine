from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.recommendation_service import get_job_recommendations


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/resume/{resume_id}",
    response_model=list[dict],
)
def read_recommendations(
    resume_id: int,
    db: Session = Depends(get_db),
):
    """Return job recommendations for a resume.

    Returns 404 if the resume does not exist.
    """
    try:
        recs = get_job_recommendations(db, resume_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return recs
