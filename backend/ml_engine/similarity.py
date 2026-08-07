"""Cosine-similarity helpers for profiles and job descriptions."""
from __future__ import annotations

from typing import Sequence

import numpy as np

from .embeddings import embed_text


def cosine_similarity(left: Sequence[float] | np.ndarray, right: Sequence[float] | np.ndarray) -> float:
    """Return cosine similarity in [-1, 1] for two non-zero vectors."""
    a = np.asarray(left, dtype=np.float32).reshape(-1)
    b = np.asarray(right, dtype=np.float32).reshape(-1)
    if a.shape != b.shape:
        raise ValueError("Vectors must have the same dimensions.")
    denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denominator == 0:
        raise ValueError("Cosine similarity is undefined for a zero vector.")
    return float(np.dot(a, b) / denominator)


def text_similarity(left: str, right: str) -> float:
    """Embed two texts and return their cosine similarity."""
    return cosine_similarity(embed_text(left), embed_text(right))


calculate_similarity = cosine_similarity
