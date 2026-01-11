import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

METADATA_FILE = "data/metadata_merged.json"
FAISS_INDEX_FILE = "data/faiss.index"

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_metadata(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_embeddings(records):
    texts = []

    for r in records:
        if "meaning" in r:
            texts.append(r["meaning"])
        else:
            texts.append(r.get("text", ""))

    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings


def main():
    records = load_metadata(METADATA_FILE)

    print(f"📘 Records loaded: {len(records)}")

    embeddings = build_embeddings(records)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_FILE)

    print("✅ FAISS index rebuilt successfully.")
    print(f"📁 Index saved to {FAISS_INDEX_FILE}")


if __name__ == "__main__":
    main()
