"""
embeddings.py
=============
Embedding generation module for the Smart India Hackathon ML Recommendation Engine.
Responsibility:
    - Load the multilingual-e5-small SentenceTransformer model (cached after first load)
    - Encode raw text (candidate profile or job description) into dense vectors
    - Normalize vectors to unit length so dot-product == cosine similarity
Author: Member 3 – Lead AI/ML & Recommendation Pipeline Engineer
"""
import logging
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# ---------------------------------------------------------------------------
# Model cache: the model is downloaded once and reused across all calls.
# Using a module-level dict keeps state between function calls without
# requiring a class instantiation from the caller's side.
# ---------------------------------------------------------------------------
_MODEL_CACHE: dict = {}
_DEFAULT_MODEL = "intfloat/multilingual-e5-small"
class EmbeddingEngine:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-small"):
        """
        Initializes the Embedding Engine.
        
        Args:
            model_name: The name of the sentence-transformer model to use.
                        Fallback: 'sentence-transformers/all-MiniLM-L6-v2'
        """
        self.model_name = model_name
        self.model = None
        self._load_model()
    def _load_model(self):
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            logger.error(f"Failed to load primary model {self.model_name}: {e}")
            logger.info("Falling back to: sentence-transformers/all-MiniLM-L6-v2")
            try:
                self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
                self.model = SentenceTransformer(self.model_name)
            except Exception as fallback_e:
