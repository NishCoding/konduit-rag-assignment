# app/indexer.py
"""
Offline Indexer:
- chunk text (700 chars / 150 overlap)
- compute TF-IDF embeddings (offline, no model download)
- store FAISS index + metadata
"""

import os
import json
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer


def chunk_text(text, chunk_size=700, overlap=150):
    step = chunk_size - overlap
    return [text[i:i + chunk_size].strip() for i in range(0, len(text), step) if text[i:i + chunk_size].strip()]


def build_index(pages_file):
    os.makedirs("data/index", exist_ok=True)
    with open(pages_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    pages = data.get("pages", {})

    corpus, meta = [], []
    for url, text in pages.items():
        for i, chunk in enumerate(chunk_text(text)):
            corpus.append(chunk)
            meta.append({"url": url, "chunk_id": i, "text": chunk})

    # TF-IDF embedding (offline)
    print("[indexer] Computing TF-IDF embeddings...")
    vectorizer = TfidfVectorizer(max_features=5000)
    embeddings = vectorizer.fit_transform(corpus).toarray().astype(np.float32)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, "data/index/faiss_index.bin")
    np.save("data/index/embeddings.npy", embeddings)
    with open("data/index/metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"[indexer] Indexed {len(corpus)} chunks with TF-IDF vectors.")
    return {"vector_count": len(corpus), "index_path": "data/index/faiss_index.bin"}
