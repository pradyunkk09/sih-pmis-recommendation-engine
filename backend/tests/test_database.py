from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.database.init_db import init_db
from app.database.database import SessionLocal
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User


def print_user(user: User) -> None:
    print(
        "User("
        f"id={user.id}, "
        f"full_name={user.full_name!r}, "
        f"email={user.email!r}, "
        f"role={user.role!r}"
        ")"
    )


def print_resume(resume: Resume) -> None:
    print(
        "Resume("
        f"id={resume.id}, "
        f"user_id={resume.user_id}, "
        f"filename={resume.filename!r}, "
        f"file_path={resume.file_path!r}"
        ")"
    )


def print_job(job: Job) -> None:
    print(
        "Job("
        f"id={job.id}, "
        f"title={job.title!r}, "
        f"company={job.company!r}, "
        f"location={job.location!r}, "
        f"employment_type={job.employment_type!r}"
        ")"
    )


def run_database_smoke_test() -> None:
    """Insert and read back one user, resume, and job record."""

    init_db()
    db = SessionLocal()

    try:
        sample_email = f"smoke.user.{uuid4().hex[:12]}@example.com"

        user = User(
            full_name="Smoke Test User",
            email=sample_email,
            password_hash="not-a-real-password-hash",
            role="candidate",
        )
        db.add(user)
        db.flush()

        resume = Resume(
            user_id=user.id,
            filename="smoke-test-resume.pdf",
            file_path="/tmp/smoke-test-resume.pdf",
            parsed_text="Python, FastAPI, SQLAlchemy",
        )
        job = Job(
            title="Backend Engineer",
            company="Example Technologies",
            description="Build and maintain production FastAPI services.",
            skills_required="Python, FastAPI, SQLAlchemy, PostgreSQL",
            location="Remote",
            employment_type="Full-time",
        )

        db.add_all([resume, job])
        db.commit()

        inserted_user = db.get(User, user.id)
        inserted_resume = db.get(Resume, resume.id)
        inserted_job = db.get(Job, job.id)

        if inserted_user is None or inserted_resume is None or inserted_job is None:
            raise RuntimeError("Smoke test records were not found after commit.")

        print("Database smoke test inserted and queried records successfully:")
        print_user(inserted_user)
        print_resume(inserted_resume)
        print_job(inserted_job)

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_database_smoke_test()
