"""
Smart India Hackathon Machine-Learning Engine.
Exports primary scoring, merit computation, and indexing interfaces.
"""

from .education_fit import calculate_education_fit
from .index import (
    BaseRetriever,
    FAISSRetriever,
    add_to_index,
    build_index,
    load_index,
    save_index,
)
from .scoring import compute_merit_score

__all__ = [
    # Index & Retrieval
    "BaseRetriever",
    "FAISSRetriever",
    "add_to_index",
    "build_index",
    "load_index",
    "save_index",
    # Scoring & Evaluation
    "compute_merit_score",
    "calculate_education_fit",
]