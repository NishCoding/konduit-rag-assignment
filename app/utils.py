
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text


def in_same_domain(base_url: str, target_url: str) -> bool:
    base = urlparse(base_url).netloc
    target = urlparse(target_url).netloc
    return target.endswith(base)


def normalize_url(base_url: str, link: str) -> str:
    absolute = urljoin(base_url, link)
    parsed = urlparse(absolute)
    return parsed._replace(fragment="").geturl()
