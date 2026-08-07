import time
import numpy as np
from Chroma_Client import search_candidates, search_jobs

dummy_vector = np.random.rand(384).tolist()

start = time.time()
res_candidates = search_candidates(dummy_vector, top_k=5)
cand_latency = (time.time() - start) * 1000

start = time.time()
res_jobs = search_jobs(dummy_vector, top_k=5)
job_latency = (time.time() - start) * 1000

print(f"Candidate Search Latency: {cand_latency:.2f} ms")
print(f"Job Search Latency: {job_latency:.2f} ms")