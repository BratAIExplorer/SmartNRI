"""
publisher.py — SmartNRI HTML Injector + Telegram Alert
Reads summaries.json, injects cards into index.html, and sends Telegram alerts for RED items.
"""

import os
import json
import logging
import datetime
import re
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR      = Path(__file__).resolve().parent.parent
DATA_DIR      = BASE_DIR / "data"
LOG_DIR       = BASE_DIR / "logs"
FRONTEND_DIR  = BASE_DIR / "frontend"
SUMMARIES_IN  = DATA_DIR / "summaries.json"
INDEX_HTML    = FRONTEND_DIR / "index.html"

LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("publisher")

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

BADGE_CLASS = {
    "GREEN":  "green",
    "ORANGE": "orange",
    "BLUE":   "blue",
    "RED":    "red",
}
BADGE_LABEL = {
    "GREEN":  "Official",
    "ORANGE": "Expert",
    "BLUE":   "Community",
    "RED":    "Alert",
}


# ── HTML card builder ──────────────────────────────────────────────────

def build_card(item: dict, delay_index: int) -> str:
    badge_cls   = BADGE_CLASS.get(item["badge"], "green")
    badge_label = BADGE_LABEL.get(item["badge"], "Official")
    bullets_html = "\n".join(
        f'          <div class="key-point">{b}</div>' for b in item["bullets"]
    )
    delay_style = f' style="animation-delay:{delay_index * 0.08:.2f}s"' if delay_index > 0 else ""
    return f"""
      <!-- Auto-generated card: {item['id']} -->
      <div class="update-card"{delay_style}>
        <div class="card-header">
          <div class="card-badge {badge_cls}">&#9679; {badge_label}</div>
          <div class="card-date">{item['date']}</div>
        </div>
        <h3 class="card-title">{item['title']}</h3>
        <p class="card-summary">{item['so_what']}</p>
        <div class="card-key-points">
          <h4>Key Points</h4>
{bullets_html}
        </div>
        <div class="card-footer">
          <div class="card-source">Source: <a href="{item['source_url']}" target="_blank" rel="noopener">{item['source_name']}</a></div>
          <a href="{item['source_url']}" class="card-cta" target="_blank" rel="noopener">Read source &#8594;</a>
        </div>
      </div>"""


# ── HTML injection ─────────────────────────────────────────────────────

CARDS_START = "<!-- AUTO-GENERATED CARDS START -->"
CARDS_END   = "<!-- AUTO-GENERATED CARDS END -->"
DATE_MARKER = "<!-- AUTO-DATE -->"


def inject_into_html(summaries: list[dict]):
    if not INDEX_HTML.exists():
        log.error(f"index.html not found at {INDEX_HTML}")
        return

    html = INDEX_HTML.read_text(encoding="utf-8")
    today_str = datetime.date.today().strftime("%-d %b %Y")

    # Build cards block
    cards_html = "\n".join(build_card(s, i) for i, s in enumerate(summaries[:5]))
    block = f"\n{CARDS_START}\n{cards_html}\n{CARDS_END}\n"

    # Replace existing block or insert before skeleton card
    if CARDS_START in html and CARDS_END in html:
        html = re.sub(
            re.escape(CARDS_START) + r".*?" + re.escape(CARDS_END),
            block.strip(),
            html,
            flags=re.DOTALL
        )
    else:
        # Insert before the skeleton card
        html = html.replace(
            '<!-- Skeleton: next update loading -->',
            f"{block}\n      <!-- Skeleton: next update loading -->"
        )

    # Update date display
    html = re.sub(r'<strong>This Week</strong> &middot; [^<]+',
                  f'<strong>This Week</strong> &middot; {today_str}', html)

    INDEX_HTML.write_text(html, encoding="utf-8")
    log.info(f"Injected {len(summaries)} cards into index.html")


# ── Telegram alerts ────────────────────────────────────────────────────

def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        log.warning("Telegram not configured — skipping alert.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        log.info("Telegram alert sent.")
    except Exception as e:
        log.error(f"Telegram send failed: {e}")


def format_telegram_alert(item: dict) -> str:
    bullets = "\n".join(f"  • {b}" for b in item["bullets"])
    return (
        f"🔴 *SmartNRI ALERT*\n\n"
        f"*{item['title']}*\n\n"
        f"{item['so_what']}\n\n"
        f"{bullets}\n\n"
        f"📎 [Read source]({item['source_url']})\n"
        f"_Source: {item['source_name']}_"
    )


# ── Weekly digest (Telegram summary) ──────────────────────────────────

def send_weekly_digest(summaries: list[dict]):
    if not summaries:
        return
    lines = ["📋 *SmartNRI — This Week's Signals*\n"]
    for i, s in enumerate(summaries[:5], 1):
        badge_emoji = {"GREEN": "🟢", "ORANGE": "🟠", "BLUE": "🔵", "RED": "🔴"}.get(s["badge"], "🟢")
        lines.append(f"{badge_emoji} *{s['title']}*\n_{s['so_what']}_\n[Source]({s['source_url']})\n")
    lines.append("_SmartNRI — Verified intelligence for Indian expats._")
    send_telegram("\n".join(lines))


# ── Main ───────────────────────────────────────────────────────────────

def run():
    if not SUMMARIES_IN.exists():
        log.warning("summaries.json not found — nothing to publish.")
        return

    with open(SUMMARIES_IN) as f:
        summaries = json.load(f)

    if not summaries:
        log.info("No summaries to publish.")
        return

    # Inject into HTML
    inject_into_html(summaries)

    # Send Telegram alerts for RED items
    red_items = [s for s in summaries if s["badge"] == "RED"]
    for item in red_items:
        send_telegram(format_telegram_alert(item))

    log.info(f"Publisher done — {len(summaries)} published, {len(red_items)} RED alerts sent.")


if __name__ == "__main__":
    run()
