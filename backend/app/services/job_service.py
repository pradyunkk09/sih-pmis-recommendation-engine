from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


def create_job(db: Session, job_data: JobCreate) -> Job:
    """
    Create a new job posting.
    """

    new_job = Job(
        title=job_data.title,
        company=job_data.company,
        description=job_data.description,
        skills_required=job_data.skills_required,
        location=job_data.location,
        employment_type=job_data.employment_type,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


def get_job_by_id(db: Session, job_id: int) -> Job | None:
    """
    Retrieve a job by its ID.
    """

    return (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )


def get_all_jobs(db: Session) -> list[Job]:
    """
    Retrieve all jobs.
    """

    return db.query(Job).all()


def update_job(
    db: Session,
    job_id: int,
    job_data: JobUpdate,
) -> Job | None:
    """
    Update an existing job.
    """

    job = get_job_by_id(db, job_id)

    if job is None:
        return None

    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    db: Session,
    job_id: int,
) -> bool:
    """
    Delete a job.
    """

    job = get_job_by_id(db, job_id)

    if job is None:
        return False

    db.delete(job)
    db.commit()

    return True