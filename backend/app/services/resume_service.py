from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.schemas.resume import ResumeCreate


def create_resume(
    db: Session,
    resume_data: ResumeCreate,
) -> Resume:
    """
    Create a new resume.
    """

    new_resume = Resume(
        user_id=resume_data.user_id,
        filename=resume_data.filename,
        file_path=resume_data.file_path,
        parsed_text=resume_data.parsed_text,
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume


def get_resume_by_id(
    db: Session,
    resume_id: int,
) -> Resume | None:
    """
    Retrieve a resume by its ID.
    """

    return (
        db.query(Resume)
        .filter(Resume.id == resume_id)
        .first()
    )


def get_resumes_by_user_id(
    db: Session,
    user_id: int,
) -> list[Resume]:
    """
    Retrieve all resumes belonging to a user.
    """

    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .all()
    )