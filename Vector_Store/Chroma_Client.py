import os
import chromadb

# Set up a persistent ChromaDB database inside the vector_store folder
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=DB_DIR)

# Get or create vector collections for both candidates and jobs
candidate_collection = client.get_or_create_collection(name="candidates")
job_collection = client.get_or_create_collection(name="jobs")

def store_candidate_vectors(candidate_ids, embeddings, metadatas, documents=None):
    """
    Stores candidate vector fingerprints created by Member 3.
    """
    candidate_collection.add(
        ids=candidate_ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )
    print(f"Stored {len(candidate_ids)} candidates into ChromaDB!")

def store_job_vectors(job_ids, embeddings, metadatas, documents=None):
    """
    Stores job vector fingerprints created by Member 3.
    """
    job_collection.add(
        ids=job_ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )
    print(f"Stored {len(job_ids)} jobs into ChromaDB!")

def search_candidates(query_vector, top_k=5):
    """
    Searches for the closest matching candidate vectors given a job embedding.
    """
    results = candidate_collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    return results

if __name__ == "__main__":
    print("ChromaDB Client initialized successfully!")
    print(f"Database location: {DB_DIR}")
    print(f"Candidates Collection Count: {candidate_collection.count()}")
    print(f"Jobs Collection Count: {job_collection.count()}")   