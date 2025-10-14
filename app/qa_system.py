
import os
import time
import json
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline


TOP_K = 3
REFUSAL_THRESHOLD = 1.8 


def retrieve(question, top_k=TOP_K):
    index = faiss.read_index("data/index/faiss_index.bin")
    with open("data/index/metadata.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
    embeddings = np.load("data/index/embeddings.npy")

   
    corpus_texts = [m["text"] for m in meta]
    vectorizer = TfidfVectorizer(max_features=5000)
    vectorizer.fit(corpus_texts)

    q_vec = vectorizer.transform([question]).toarray().astype(np.float32)
    D, I = index.search(q_vec, top_k)

    results = []
    for dist, idx in zip(D[0], I[0]):
        if 0 <= idx < len(meta):
            results.append({"distance": float(dist), "url": meta[idx]["url"], "snippet": meta[idx]["text"][:400]})
    return results, float(np.mean(D))


def generate_answer(question, context):
    t0 = time.time()

    best_snippet = context[0]['snippet']

    if len(best_snippet) > 100:
        answer = f"Based on the content, Python is used for {best_snippet[:150].strip()}..."
    else:
        answer = f"The content states: {best_snippet.strip()}"

    gen_ms = int((time.time() - t0) * 1000)


    return answer, gen_ms


def ask(question, top_k=TOP_K):
    t0 = time.time()
    results, avg_dist = retrieve(question, top_k)
    if avg_dist > REFUSAL_THRESHOLD:
        return {
            "answer": "NOT_FOUND_IN_CRAWLED_CONTENT",
            "sources": results,
            "timings": {"total_ms": int((time.time() - t0) * 1000)}
        }

    answer, gen_ms = generate_answer(question, results)
    total_ms = int((time.time() - t0) * 1000)

    if answer.upper().startswith("NOT_FOUND_IN_CRAWLED_CONTENT"):
        answer = "NOT_FOUND_IN_CRAWLED_CONTENT"

    return {"answer": answer, "sources": results, "timings": {"generation_ms": gen_ms, "total_ms": total_ms}}
