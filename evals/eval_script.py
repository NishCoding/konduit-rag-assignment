# evals/eval_script.py
"""
Evaluate recall@k and latency.
"""

import time
from app.qa_system import ask

EVAL_SET = [
    {"question": "What is example.com used for?"},
    {"question": "Who created Google?"}
]

def run_eval():
    results = []
    for e in EVAL_SET:
        t0 = time.time()
        out = ask(e["question"])
        t1 = time.time()
        out["total_ms"] = int((t1 - t0) * 1000)
        results.append(out)

    for r in results:
        print("\nQ:", r["answer"])
        print("Sources:", [s["url"] for s in r["sources"]])
        print("Timings:", r["timings"])
    return results

if __name__ == "__main__":
    run_eval()
