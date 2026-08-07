"""Education qualification matching for internship recommendations."""
from __future__ import annotations

import re
from typing import Final

_QUALIFICATION_TIERS: Final[dict[str, int]] = {
    "10th": 1,
    "high school": 1,
    "12th": 2,
    "higher secondary": 2,
    "iti": 3,
    "diploma": 4,
    "graduate": 5,
    "bachelors": 5,
    "bachelor": 5,
    "undergraduate": 5,
    "postgraduate": 6,
    "post graduate": 6,
    "masters": 6,
    "master": 6,
    "pg": 6,
}
_UNKNOWN_QUALIFICATION_SCORE: Final[float] = 0.3


def qualification_rank(qualification: str | None) -> int | None:
    """Return a qualification's ordinal tier, or ``None`` when it is unknown."""
    if not isinstance(qualification, str) or not qualification.strip():
        return None

    normalised = re.sub(r"[._/-]+", " ", qualification.casefold()).strip()
    normalised = re.sub(r"\s+", " ", normalised)
    if normalised in _QUALIFICATION_TIERS:
        return _QUALIFICATION_TIERS[normalised]

    # Accept common descriptive forms such as "Bachelor of Engineering" without
    # treating arbitrary text as a qualification.
    tokens = set(normalised.split())
    if "bachelor" in tokens or "bachelors" in tokens or "graduate" in tokens:
        return 5
    if "master" in tokens or "masters" in tokens or "postgraduate" in tokens:
        return 6
    return None


def calculate_education_fit(candidate_qual: str, job_min_qual: str) -> float:
    """Score education fit from ordinal qualification distance.

    Unknown or missing values receive the neutral fallback score of ``0.3``.
    A candidate below the stated minimum receives ``0.0``.
    """
    candidate_rank = qualification_rank(candidate_qual)
    job_rank = qualification_rank(job_min_qual)
    if candidate_rank is None or job_rank is None:
        return _UNKNOWN_QUALIFICATION_SCORE

    distance = candidate_rank - job_rank
    if distance == 0:
        return 1.0
    if distance < 0:
        return 0.0
    if distance == 1:
        return 0.9
    if distance == 2:
        return 0.8
    return 0.7
