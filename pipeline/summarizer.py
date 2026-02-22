"""
summarizer.py — SmartNRI LLM Processor
Takes raw_content.json and produces badge-tagged, bullet-point summaries.
Outputs: data/summaries.json

Rules:
- Uses OpenAI gpt-4o-mini OR Gemini gemini-1.5-flash (configured via .env)
- Temperature 0.1 (factual, not creative)
- If LLM cannot summarise accurately → {"skip": true}
- If API fails → raise exception (watchdog catches this)
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR     = Path(__file__).resolve().parent.parent
DATA_DIR     = BASE_DIR / "data"
LOG_DIR      = BASE_DIR / "logs"
RAW_INPUT    = DATA_DIR / "raw_content.json"
SUMMARIES_OUT = DATA_DIR / "summaries.json"

LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("summarizer")

# ── LLM config ────────────────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()  # "openai" or "gemini"
OPENAI_KEY   = os.getenv("OPENAI_API_KEY", "")
GEMINI_KEY   = os.getenv("GEMINI_API_KEY", "")

SYSTEM_PROMPT = """You are a compliance guide for Indian expats (NRIs) living abroad.
Your job is to summarise government updates into clear, actionable intelligence.

Rules:
1. Write EXACTLY 3 bullet points. Each bullet is one actionable sentence.
2. Start each bullet with a strong verb: Review, Convert, File, Check, Declare, Ensure, Confirm.
3. Do NOT add information not present in the source text.
4. Do NOT give legal or financial advice — only state what the rule/circular says.
5. Write one clear "So What?" sentence (max 25 words) summarising the impact.
6. Suggest a badge: GREEN (official update), ORANGE (expert/advisory), BLUE (community), RED (urgent action required).
7. If you cannot summarise accurately from the text provided, respond with exactly: {"skip": true}

Respond ONLY with valid JSON in this format:
{
  "title": "Short punchy headline (max 12 words)",
  "so_what": "One sentence on why this matters to NRIs.",
  "bullets": ["Bullet 1.", "Bullet 2.", "Bullet 3."],
  "badge": "GREEN",
  "skip": false
}"""


def call_openai(raw_text: str, source_url: str) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    user_msg = f"Source URL: {source_url}\n\nContent:\n{raw_text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def call_gemini(raw_text: str, source_url: str) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    user_msg = f"{SYSTEM_PROMPT}\n\nSource URL: {source_url}\n\nContent:\n{raw_text}"
    response = model.generate_content(
        user_msg,
        generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
    )
    return json.loads(response.text)


def summarise(item: dict) -> dict | None:
    """Call LLM and return structured summary or None if skipped."""
    try:
        if LLM_PROVIDER == "gemini":
            result = call_gemini(item["raw_text"], item["source_url"])
        else:
            result = call_openai(item["raw_text"], item["source_url"])

        if result.get("skip"):
            log.info(f"  SKIPPED by LLM: {item['title'][:60]}")
            return None

        # Merge with source metadata
        return {
            "id":          item["id"],
            "source_id":   item["source_id"],
            "source_name": item["source_name"],
            "source_url":  item["source_url"],
            "domain":      item["domain"],
            "tier":        item["tier"],
            "date":        item["date_found"],
            "badge":       result.get("badge", item.get("badge", "green")).upper(),
            "title":       result.get("title", item["title"]),
            "so_what":     result.get("so_what", ""),
            "bullets":     result.get("bullets", []),
            "skip":        False
        }

    except Exception as e:
        log.error(f"LLM call failed for {item.get('id')}: {e}")
        raise  # Let watchdog catch this


def run() -> list[dict]:
    if not RAW_INPUT.exists():
        log.warning("raw_content.json not found — nothing to summarise.")
        return []

    with open(RAW_INPUT) as f:
        raw_items = json.load(f)

    if not raw_items:
        log.info("No new items to summarise.")
        with open(SUMMARIES_OUT, "w") as f:
            json.dump([], f)
        return []

    log.info(f"Summarising {len(raw_items)} items via {LLM_PROVIDER.upper()}...")
    summaries = []

    for item in raw_items:
        log.info(f"  Processing: {item['title'][:60]}")
        result = summarise(item)
        if result:
            summaries.append(result)

    with open(SUMMARIES_OUT, "w") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

    log.info(f"Summariser done — {len(summaries)} summaries saved.")
    return summaries


if __name__ == "__main__":
    run()
