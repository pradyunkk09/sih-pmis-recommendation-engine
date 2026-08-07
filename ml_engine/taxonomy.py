"""Load and query the package-local skills taxonomy."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

_TAXONOMY_PATH = Path(__file__).with_name("taxonomy_graph.json")


def load_taxonomy(path: str | Path | None = None) -> dict[str, Any]:
    """Load a taxonomy JSON object; package-relative by default."""
    source = Path(path) if path is not None else _TAXONOMY_PATH
    with source.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("Taxonomy JSON must contain an object at its root.")
    return data


def _walk(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key, child in value.items():
            yield str(key)
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def taxonomy_terms(taxonomy: Mapping[str, Any] | None = None) -> set[str]:
    """Return case-folded terms from arbitrary nested taxonomy JSON."""
    return {term.casefold().strip() for term in _walk(taxonomy or load_taxonomy()) if term.strip()}


def extract_skills(text: str, taxonomy: Mapping[str, Any] | None = None) -> list[str]:
    """Find known taxonomy terms occurring in text, longest match first."""
    haystack = text.casefold()
    return [term for term in sorted(taxonomy_terms(taxonomy), key=len, reverse=True) if term in haystack]


def taxonomy_similarity(left: str, right: str, taxonomy: Mapping[str, Any] | None = None) -> float:
    """Compute Jaccard overlap of taxonomy terms extracted from two texts."""
    left_terms, right_terms = set(extract_skills(left, taxonomy)), set(extract_skills(right, taxonomy))
    union = left_terms | right_terms
    return len(left_terms & right_terms) / len(union) if union else 0.0


def taxonomy_score(left: str, right: str, taxonomy: Mapping[str, Any] | None = None) -> float:
    """Compatibility name for the taxonomy-based skill-match score."""
    return taxonomy_similarity(left, right, taxonomy)
