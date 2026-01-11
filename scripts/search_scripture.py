import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# File paths
INDEX_FILE = "data/faiss.index"
META_FILE = "data/metadata.json"

# Load embedding model
print("🔄 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
print("📦 Loading FAISS index...")
index = faiss.read_index(INDEX_FILE)

# Load metadata
with open(META_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

print(f"📖 Loaded metadata for {len(metadata)} records")

# Function to search scriptures
def search_scripture(query, top_k=5):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results


# ---- ASK A QUESTION HERE ----
question = "What does Dharma say about duty?"

print("\n❓ Question:", question)
print("\n📜 Relevant Scripture Passages:\n")

results = search_scripture(question)

for i, res in enumerate(results, 1):
    print(f"{i}. [{res['book'].upper()}] {res['text']}\n")
