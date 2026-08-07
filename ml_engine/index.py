"""FAISS index lifecycle and retrieval abstractions."""
from __future__ import annotations

from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from .embeddings import embed_batch, embed_text

_INDEX_FILENAME = "internships.faiss"
_META_FILENAME = "internships_meta.json"


def _faiss() -> Any:
    try:
        import faiss
    except ImportError as exc:
        raise RuntimeError("faiss-cpu is required to use the vector index.") from exc
    return faiss


def _normalise(vector: np.ndarray) -> np.ndarray:
    array = np.asarray(vector, dtype=np.float32)
    if array.ndim == 1:
        array = array.reshape(1, -1)
    if array.ndim != 2:
        raise ValueError("Embeddings must be one- or two-dimensional arrays.")
    norms = np.linalg.norm(array, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Embeddings must not contain zero vectors.")
    return array / norms


class BaseRetriever(ABC):
    @abstractmethod
    def search(self, query: str | np.ndarray, k: int = 5) -> list[tuple[dict[str, Any], float]]:
        """Return the k most similar metadata records and their scores."""

    @abstractmethod
    def add(self, internship: Mapping[str, Any], embedding: np.ndarray | None = None) -> None:
        """Add a metadata record, optionally with a precomputed embedding."""


class FAISSRetriever(BaseRetriever):
    def __init__(self, index: Any, metadata: Sequence[Mapping[str, Any]]) -> None:
        if index.ntotal != len(metadata):
            raise ValueError("FAISS vector count must equal metadata count.")
        self.index = index
        self.metadata = [dict(item) for item in metadata]

    def search(self, query: str | np.ndarray, k: int = 5) -> list[tuple[dict[str, Any], float]]:
        if k < 1:
            return []
        vector = embed_text(query) if isinstance(query, str) else np.asarray(query)
        vector = _normalise(vector)
        if vector.shape[1] != self.index.d:
            raise ValueError(f"Expected an embedding with {self.index.d} dimensions.")
        scores, ids = self.index.search(vector, min(k, self.index.ntotal))
        return [(dict(self.metadata[i]), float(score)) for score, i in zip(scores[0], ids[0]) if i >= 0]

    def add(self, internship: Mapping[str, Any], embedding: np.ndarray | None = None) -> None:
        item = dict(internship)
        vector = embedding if embedding is not None else embed_text(_internship_text(item))
        vector = _normalise(vector)
        if vector.shape != (1, self.index.d):
            raise ValueError(f"Expected one embedding with {self.index.d} dimensions.")
        self.index.add(vector)
        self.metadata.append(item)


def _internship_text(item: Mapping[str, Any]) -> str:
    for key in ("description", "job_description", "jd", "text", "title"):
        if item.get(key):
            return str(item[key])
    raise ValueError("Each internship needs description, job_description, jd, text, or title.")


def build_index(internships: Sequence[Mapping[str, Any]]) -> FAISSRetriever:
    records = [dict(item) for item in internships]
    if not records:
        raise ValueError("Cannot build an index from an empty internship list.")
    vectors = _normalise(embed_batch([_internship_text(item) for item in records]))
    faiss = _faiss()
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return FAISSRetriever(index, records)


def save_index(retriever: FAISSRetriever, directory: str | Path) -> None:
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    _faiss().write_index(retriever.index, str(target / _INDEX_FILENAME))
    (target / _META_FILENAME).write_text(json.dumps(retriever.metadata, ensure_ascii=False), encoding="utf-8")


def load_index(directory: str | Path) -> FAISSRetriever:
    source = Path(directory)
    metadata = json.loads((source / _META_FILENAME).read_text(encoding="utf-8"))
    if not isinstance(metadata, list):
        raise ValueError("Index metadata must be a JSON list.")
    return FAISSRetriever(_faiss().read_index(str(source / _INDEX_FILENAME)), metadata)


def add_to_index(retriever: BaseRetriever, internship: Mapping[str, Any]) -> None:
    retriever.add(internship)
