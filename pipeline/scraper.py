"""
scraper.py — SmartNRI Data Fetcher
Fetches content from whitelisted Tier 1 government sources.
Outputs: data/raw_content.json

Rules:
- Only fetch from sources listed in sources.json
- Skip if content hash unchanged since last run
- Max 5 new items per run
- Log all errors to logs/scraper_errors.log
"""

import os
import json
import hashlib
import logging
import datetime
import time
from pathlib import Path

import requests
import feedparser
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
DATA_DIR   = BASE_DIR / "data"
LOG_DIR    = BASE_DIR / "logs"
SOURCES_FILE   = Path(__file__).resolve().parent / "sources.json"
RAW_OUTPUT     = DATA_DIR / "raw_content.json"
HASH_CACHE     = DATA_DIR / "content_hashes.json"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scraper_errors.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("scraper")

# ── Constants ──────────────────────────────────────────────────────────
MAX_ITEMS    = 5
REQUEST_TIMEOUT = 15
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; SmartNRI-Bot/1.0; "
        "+https://github.com/BratAIExplorer/SmartNRI)"
    )
}


# ── Helpers ────────────────────────────────────────────────────────────

def load_sources() -> list:
    with open(SOURCES_FILE) as f:
        return [s for s in json.load(f) if s.get("active")]


def load_hash_cache() -> dict:
    if HASH_CACHE.exists():
        with open(HASH_CACHE) as f:
            return json.load(f)
    return {}


def save_hash_cache(cache: dict):
    with open(HASH_CACHE, "w") as f:
        json.dump(cache, f, indent=2)


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


# ── Session & Retry ───────────────────────────────────────────────────

class LegacySSLAdapter(requests.adapters.HTTPAdapter):
    """Custom adapter to handle 'Unsafe Legacy Renegotiation Disabled' errors."""
    def init_poolmanager(self, *args, **kwargs):
        import ssl
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

def get_session():
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter
    
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    # Mount legacy adapter for specific domains that fail SSL
    legacy_adapter = LegacySSLAdapter(max_retries=retry_strategy)
    session.mount("https://www.passportindia.gov.in", legacy_adapter)
    
    return session

_session = get_session()

def safe_get(url: str) -> requests.Response | None:
    try:
        r = _session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r
    except requests.RequestException as e:
        log.error(f"GET failed for {url}: {e}")
        return None


def slugify(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "-")
        .replace("/", "-")
        [:60]
    )


# ── Scrapers ───────────────────────────────────────────────────────────

def scrape_html(source: dict) -> list[dict]:
    """Generic HTML scraper — extracts headings + paragraphs."""
    resp = safe_get(source["url"])
    if not resp:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try common patterns for gov announcement pages
    items = []
    candidates = (
        soup.select("article") or
        soup.select(".announcement, .news-item, .press-release, .update") or
        soup.select("li.item, li.news") or
        []
    )

    # Fallback: grab all headings with adjacent text
    if not candidates:
        for tag in soup.find_all(["h2", "h3", "h4"]):
            text = tag.get_text(strip=True)
            sibling = tag.find_next_sibling(["p", "div"])
            body = sibling.get_text(strip=True) if sibling else ""
            if len(text) > 20:
                items.append({
                    "title": text,
                    "raw_text": body,
                    "link": source["url"]
                })
        return items[:MAX_ITEMS]

    for el in candidates[:MAX_ITEMS]:
        title_tag = el.find(["h2", "h3", "h4", "a"])
        title = title_tag.get_text(strip=True) if title_tag else el.get_text(strip=True)[:80]
        link_tag = el.find("a", href=True)
        link = link_tag["href"] if link_tag else source["url"]
        if link.startswith("/"):
            from urllib.parse import urlparse
            base = urlparse(source["url"])
            link = f"{base.scheme}://{base.netloc}{link}"
        body = el.get_text(separator=" ", strip=True)
        items.append({"title": title, "raw_text": body, "link": link})

    return items


def scrape_rss(source: dict) -> list[dict]:
    """RSS/Atom feed scraper."""
    feed = feedparser.parse(source["url"])
    items = []
    for entry in feed.entries[:MAX_ITEMS]:
        title = entry.get("title", "")
        summary = entry.get("summary", entry.get("description", ""))
        link = entry.get("link", source["url"])
        # Strip HTML tags from summary
        clean = BeautifulSoup(summary, "html.parser").get_text(separator=" ", strip=True)
        items.append({"title": title, "raw_text": clean, "link": link})
    return items


# ── Main ───────────────────────────────────────────────────────────────

def run() -> list[dict]:
    sources    = load_sources()
    hash_cache = load_hash_cache()
    results    = []
    new_hashes = dict(hash_cache)
    today      = datetime.date.today().isoformat()

    log.info(f"Scraper started — {len(sources)} active sources")

    for source in sources:
        if len(results) >= MAX_ITEMS:
            log.info("Max items reached, stopping.")
            break

        log.info(f"Fetching: {source['name']} ({source['url']})")

        if source["scrape_method"] == "rss":
            raw_items = scrape_rss(source)
        else:
            raw_items = scrape_html(source)

        if not raw_items:
            log.warning(f"No items found for {source['name']}")
            continue

        for item in raw_items:
            if len(results) >= MAX_ITEMS:
                break

            combined = (item["title"] + item["raw_text"]).strip()
            if len(combined) < 50:
                continue  # Too short, skip

            content_hash = hash_content(combined)
            cache_key = f"{source['id']}:{slugify(item['title'])}"

            if hash_cache.get(cache_key) == content_hash:
                log.info(f"  Unchanged: {item['title'][:60]}")
                continue

            record = {
                "id": f"{source['id']}-{today}-{slugify(item['title'])}",
                "source_id": source["id"],
                "source_name": source["name"],
                "source_url": item["link"],
                "domain": source["domain"],
                "tier": source["tier"],
                "badge": source["badge"],
                "topics": source["topics"],
                "title": item["title"],
                "raw_text": item["raw_text"][:3000],  # cap at 3000 chars for LLM
                "date_found": today,
                "content_hash": content_hash
            }

            results.append(record)
            new_hashes[cache_key] = content_hash
            log.info(f"  NEW: {item['title'][:60]}")

        time.sleep(1)  # polite crawl delay between sources

    # Save outputs
    with open(RAW_OUTPUT, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    save_hash_cache(new_hashes)

    log.info(f"Scraper done — {len(results)} new items saved to {RAW_OUTPUT}")
    return results


if __name__ == "__main__":
    run()
