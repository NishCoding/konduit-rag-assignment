
import os
import json
import time
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from app.utils import clean_html, in_same_domain, normalize_url


def crawl(start_url: str, max_pages: int = 30, crawl_delay: float = 1.0):
    visited, to_visit = set(), [start_url]
    pages = {}

    parsed_domain = urlparse(start_url).netloc.replace("www.", "")
    os.makedirs("data/pages", exist_ok=True)

    print(f"[crawler] Starting crawl from {start_url} (limit {max_pages})")

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            resp = requests.get(url, timeout=10, headers={"User-Agent": "RAGBot/1.0"})
            if "text/html" not in resp.headers.get("Content-Type", ""):
                continue
            text = clean_html(resp.text)
            pages[url] = text
            visited.add(url)
            print(f"[crawler] ({len(visited)}/{max_pages}) {url}")

            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.find_all("a", href=True):
                next_url = normalize_url(url, link["href"])
                if in_same_domain(start_url, next_url) and next_url not in visited and next_url not in to_visit:
                    to_visit.append(next_url)

            time.sleep(crawl_delay)
        except Exception as e:
            print(f"[crawler] Skipped {url}: {e}")
            continue

    out_file = f"data/pages/crawl_{parsed_domain}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"pages": pages}, f, indent=2)

    print(f"[crawler] Done. Crawled {len(visited)} pages → {out_file}")
    return {"page_count": len(visited), "urls": list(visited), "output": out_file}
