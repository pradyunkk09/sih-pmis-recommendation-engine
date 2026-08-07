"""
index.py
========
FAISS vector index lifecycle and retrieval abstraction layer.
Provides:
  - BaseRetriever  : Abstract interface — the only contract scoring.py touches.
  - FAISSRetriever : Concrete local FAISS implementation (IndexFlatIP).
  - build_index()  : Build a FAISSRetriever from a list of internship dicts.
  - save_index()   : Persist index + metadata sidecar to disk.
  - load_index()   : Restore FAISSRetriever from disk.
  - add_to_index() : Incrementally add a single internship.
Retrieval abstraction design:
  scoring.py ONLY calls retriever.search() and retriever.add().
  When Member 4 integrates ChromaDB/Qdrant, they implement BaseRetriever
  in their own module — zero changes required in scoring.py, embeddings.py,
  taxonomy.py, or education_fit.py.
FAISS details:
  - Index type: IndexFlatIP (exact inner product search)
  - Vectors are L2-normalized before insertion, so inner product = cosine similarity.
  - Metadata (including pre-computed jd_embedding) stored as a JSON sidecar
    file, index-aligned with FAISS vectors.
"""
from __future__ import annotations
import abc
import json
from pathlib import Path
import faiss
import logging
from typing import List, Tuple
import numpy as np
import faiss
from .embeddings import embed_batch, embed_text
logger = logging.getLogger(__name__)
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_VECTOR_DIM = 384
_INDEX_FILENAME = "internships.faiss"
_META_FILENAME = "internships_meta.json"