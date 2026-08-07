"""Recommendation service integrating the FastAPI backend with the ml_engine.

Provides a single function get_job_recommendations(db, resume_id) that returns
up to 5 job recommendations sorted by computed merit score.

This keeps the implementation intentionally simple for a hackathon MVP.
"""
from __future__ import annotations

from typing import Any, Dict, List

from sqlalchemy.orm import Session

from ml_engine import compute_merit_score

from app.models.resume import Resume
from app.models.job import Job


def get_job_recommendations(db: Session, resume_id: int) -> List[Dict[str, Any]]:
    """Return up to 5 job recommendations for the given resume.

    Args:
        db: SQLAlchemy Session
        resume_id: Resume primary key

    Returns:
        List of dicts containing job_id, title, company, merit_score and score_breakdown
    """
    # Read the resume
    resume = db.query(Resume).filter(Resume.id == resume_id).one_or_none()
    if resume is None:
        raise ValueError(f"Resume with id={resume_id} not found")

    # Read all jobs
    jobs = db.query(Job).all()
    if not jobs:
        return []

    recommendations: List[Dict[str, Any]] = []

    for job in jobs:
        # Build candidate data from the Resume model. Keys chosen to match ml_engine expectations.
        candidate_data: Dict[str, Any] = {
            "skills": resume.skills,
            "profile_summary": resume.profile_summary,
            "resume_text": resume.parsed_text,
            "district": resume.district,
            "state": resume.state,
            "qualification": resume.qualification,
        }

        # Build job data from the Job model. Keys chosen to match ml_engine expectations.
        job_data: Dict[str, Any] = {
            "required_skills": getattr(job, "skills_required", None),
            "description": getattr(job, "description", None),
            "title": getattr(job, "title", None),
            "company": getattr(job, "company", None),
            "district": getattr(job, "district", None),
            "state": getattr(job, "state", None),
        }

        # Compute merit score using the ml engine
        score_result = compute_merit_score(candidate_data, job_data)

        recommendations.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "merit_score": score_result.get("merit_score"),
                "score_breakdown": score_result.get("breakdown"),
            }
        )

    # Sort by merit_score descending and return top 5
    recommendations.sort(key=lambda r: (r.get("merit_score") is not None, r.get("merit_score")), reverse=True)
    return recommendations[:5]
