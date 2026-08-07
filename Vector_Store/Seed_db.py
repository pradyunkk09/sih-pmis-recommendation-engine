import json
import os
import numpy as np
from Chroma_Client import store_candidate_vectors, store_job_vectors

# Locate json files relative to this script
BASE_DIR = os.path.dirname(__file__)
CANDIDATES_PATH = os.path.join(BASE_DIR, "..", "Data Pipeline", "candidates.json")
JOBS_PATH = os.path.join(BASE_DIR, "..", "Data Pipeline", "jobs.json")

def seed():
    # 1. Store Candidates
    if os.path.exists(CANDIDATES_PATH):
        with open(CANDIDATES_PATH, "r") as f:
            candidates = json.load(f)

        ids = [str(c.get("id", i)) for i, c in enumerate(candidates)]
        # Generate 384-dimensional vector placeholders (multilingual-e5-small dimensions)
        embeddings = [np.random.rand(384).tolist() for _ in candidates]
        metadatas = [
            {
                "qualification": str(c.get("qualification", "")),
                "district": str(c.get("district", ""))
            }
            for c in candidates
        ]

        store_candidate_vectors(ids, embeddings, metadatas)

    # 2. Store Jobs
    if os.path.exists(JOBS_PATH):
        with open(JOBS_PATH, "r") as f:
            jobs = json.load(f)

        ids = [str(j.get("id", i)) for i, j in enumerate(jobs)]
        embeddings = [np.random.rand(384).tolist() for _ in jobs]
        metadatas = [
            {
                "title": str(j.get("title", "")),
                "district": str(j.get("district", ""))
            }
            for j in jobs
        ]

        store_job_vectors(ids, embeddings, metadatas)

if __name__ == "__main__":
    seed()