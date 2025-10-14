# main.py
"""
CLI driver: crawl → index → ask
"""

import argparse
from app.crawler import crawl
from app.indexer import build_index
from app.qa_system import ask

def main():
    p = argparse.ArgumentParser(description="Mini RAG CLI")
    p.add_argument("--crawl", help="Starting URL to crawl")
    p.add_argument("--max_pages", type=int, default=10)
    p.add_argument("--crawl_delay", type=float, default=1.0)
    p.add_argument("--index", help="Path to pages JSON for indexing")
    p.add_argument("--ask", help="Question to ask")
    args = p.parse_args()

    if args.crawl:
        crawl_info = crawl(args.crawl, args.max_pages, args.crawl_delay)
        print(crawl_info)
        if not args.index:
            args.index = crawl_info["output"]

    if args.index:
        idx_info = build_index(args.index)
        print(idx_info)

    if args.ask:
        response = ask(args.ask)
        print("\n=== ANSWER ===")
        print(response)

if __name__ == "__main__":
    main()
