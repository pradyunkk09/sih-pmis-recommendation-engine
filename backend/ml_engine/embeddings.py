"""Embedding helpers shared by the ML engine modules."""
from __future__ import annotations

import logging
from typing import Sequence

import numpy as np

logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "intfloat/multilingual-e5-small"
_MODEL_CACHE: dict[str, object] = {}


def _model(model_name: str = _DEFAULT_MODEL) -> object:
    """Return a cached SentenceTransformer without loading it at import time."""
    if model_name not in _MODEL_CACHE:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # keep package imports useful before install
            raise RuntimeError(
                "sentence-transformers is required for embedding generation. "
                "Install ml_engine/requirements.txt."
            ) from exc
        logger.info("Loading embedding model: %s", model_name)
        _MODEL_CACHE[model_name] = SentenceTransformer(model_name)
    return _MODEL_CACHE[model_name]


def _normalise(vectors: np.ndarray) -> np.ndarray:
    vectors = np.asarray(vectors, dtype=np.float32)
    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.maximum(norms, np.finfo(np.float32).eps)


def embed_batch(texts: Sequence[str], *, model_name: str = _DEFAULT_MODEL) -> np.ndarray:
    """Encode text into L2-normalised float32 vectors."""
    values = [str(text or "") for text in texts]
    if not values:
        return np.empty((0, 0), dtype=np.float32)
    encoder = _model(model_name)
    vectors = encoder.encode(values, convert_to_numpy=True, show_progress_bar=False)
    return _normalise(vectors)


def embed_text(text: str, *, model_name: str = _DEFAULT_MODEL) -> np.ndarray:
    """Encode one text value and return a one-dimensional vector."""
    return embed_batch([text], model_name=model_name)[0]
