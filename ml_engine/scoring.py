"""Central merit-scoring entry point for the recommendation engine."""
from __future__ import annotations

import re
from typing import Any, Mapping

from .education_fit import calculate_education_fit
from .embeddings import embed_text
from .similarity import cosine_similarity
from .taxonomy import taxonomy_score

_NEIGHBOURING_STATES: dict[str, set[str]] = {
    "andhra pradesh": {"telangana", "karnataka", "odisha", "tamil nadu", "chhattisgarh"},
    "assam": {"arunachal pradesh", "nagaland", "manipur", "mizoram", "meghalaya", "west bengal", "tripura"},
    "bihar": {"jharkhand", "uttar pradesh", "west bengal"},
    "chhattisgarh": {"andhra pradesh", "jharkhand", "madhya pradesh", "maharashtra", "odisha", "telangana", "uttar pradesh"},
    "delhi": {"haryana", "uttar pradesh", "rajasthan"},
    "gujarat": {"rajasthan", "madhya pradesh", "maharashtra"},
    "haryana": {"delhi", "himachal pradesh", "punjab", "rajasthan", "uttar pradesh", "uttarakhand"},
    "karnataka": {"andhra pradesh", "goa", "kerala", "maharashtra", "tamil nadu", "telangana"},
    "kerala": {"karnataka", "tamil nadu"},
    "madhya pradesh": {"chhattisgarh", "gujarat", "maharashtra", "rajasthan", "uttar pradesh"},
    "maharashtra": {"chhattisgarh", "goa", "gujarat", "karnataka", "madhya pradesh", "telangana"},
    "odisha": {"andhra pradesh", "chhattisgarh", "jharkhand", "west bengal"},
    "punjab": {"haryana", "himachal pradesh", "rajasthan"},
    "rajasthan": {"delhi", "gujarat", "haryana", "madhya pradesh", "punjab", "uttar pradesh"},
    "tamil nadu": {"andhra pradesh", "karnataka", "kerala"},
    "telangana": {"andhra pradesh", "chhattisgarh", "karnataka", "maharashtra"},
    "uttar pradesh": {"bihar", "chhattisgarh", "delhi", "haryana", "madhya pradesh", "rajasthan", "uttarakhand"},
    "west bengal": {"assam", "bihar", "jharkhand", "odisha", "sikkim"},
}


def _normalise_location(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").casefold()).strip()


def calculate_location_score(
    candidate_district: str | None,
    job_district: str | None,
    candidate_state: str | None = None,
    job_state: str | None = None,
) -> float:
    """Score location compatibility: district, state/adjacent state, then fallback."""
    candidate_district = _normalise_location(candidate_district)
    job_district = _normalise_location(job_district)
    if candidate_district and candidate_district == job_district:
        return 1.0

    candidate_state = _normalise_location(candidate_state)
    job_state = _normalise_location(job_state)
    if candidate_state and job_state:
        if candidate_state == job_state or job_state in _NEIGHBOURING_STATES.get(candidate_state, set()):
            return 0.7
    return 0.4


def _first_text(record: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (list, tuple, set)):
            values = [str(item).strip() for item in value if str(item).strip()]
            if values:
                return ", ".join(values)
    return ""


def _bounded(score: float) -> float:
    return max(0.0, min(1.0, float(score)))


def compute_merit_score(candidate_data: dict, job_data: dict) -> dict:
    """Compute merit score and return a complete, auditable score breakdown.

    Accepted text fields include ``skills``, ``profile_summary`` and ``resume_text``
    for a candidate, and ``required_skills``, ``description`` and
    ``job_description`` for a job. Missing text is treated as no match.
    """
    if not isinstance(candidate_data, Mapping) or not isinstance(job_data, Mapping):
        raise TypeError("candidate_data and job_data must be dictionaries.")

    candidate_text = _first_text(candidate_data, "skills", "profile_summary", "resume_text", "text")
    job_text = _first_text(job_data, "required_skills", "skills", "description", "job_description", "jd", "text")
    if candidate_text and job_text:
        semantic_sim = _bounded(cosine_similarity(embed_text(candidate_text), embed_text(job_text)))
        taxonomy_score_value = _bounded(taxonomy_score(candidate_text, job_text))
    else:
        semantic_sim = taxonomy_score_value = 0.0

    skill_match_score = 0.6 * semantic_sim + 0.4 * taxonomy_score_value
    location_score = calculate_location_score(
        _first_text(candidate_data, "district", "candidate_district"),
        _first_text(job_data, "district", "job_district"),
        _first_text(candidate_data, "state", "candidate_state"),
        _first_text(job_data, "state", "job_state"),
    )
    education_fit_score = calculate_education_fit(
        _first_text(candidate_data, "qualification", "education", "candidate_qual"),
        _first_text(job_data, "minimum_qualification", "min_qualification", "job_min_qual", "qualification"),
    )
    merit_score = 0.50 * skill_match_score + 0.20 * location_score + 0.15 * education_fit_score

    return {
        "merit_score": round(merit_score, 6),
        "breakdown": {
            "semantic_sim": round(semantic_sim, 6),
            "taxonomy_score": round(taxonomy_score_value, 6),
            "skill_match_score": round(skill_match_score, 6),
            "location_score": round(location_score, 6),
            "education_fit_score": round(education_fit_score, 6),
        },
    }
