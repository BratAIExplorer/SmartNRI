"""
watchdog.py — SmartNRI Health Monitor
Detects pipeline failures and sends Telegram/email alerts.
Called at the end of every pipeline run by main.py.
"""

import os
import json
import logging
import datetime
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR      = Path(__file__).resolve().parent.parent
DATA_DIR      = BASE_DIR / "data"
LOG_DIR       = BASE_DIR / "logs"
SUMMARIES_FILE = DATA_DIR / "summaries.json"
INDEX_HTML    = BASE_DIR / "frontend" / "index.html"
PIPELINE_LOG  = LOG_DIR / "pipeline.log"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("watchdog")

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
SMTP_HOST        = os.getenv("SMTP_HOST", "")
SMTP_PORT        = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER        = os.getenv("SMTP_USER", "")
SMTP_PASS        = os.getenv("SMTP_PASS", "")
ALERT_EMAIL      = os.getenv("ALERT_EMAIL", "")

MAX_INDEX_AGE_HOURS = 28


def get_last_log_lines(n: int = 15) -> str:
    if not PIPELINE_LOG.exists():
        return "(no log file found)"
    lines = PIPELINE_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-n:])


def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"},
            timeout=10
        ).raise_for_status()
    except Exception as e:
        log.error(f"Watchdog Telegram failed: {e}")


def send_email(subject: str, body: str):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, ALERT_EMAIL]):
        return
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"]    = SMTP_USER
        msg["To"]      = ALERT_EMAIL
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(SMTP_USER, ALERT_EMAIL, msg.as_string())
        log.info("Watchdog email sent.")
    except Exception as e:
        log.error(f"Watchdog email failed: {e}")


def alert(reason: str):
    log_tail = get_last_log_lines()
    msg = (
        f"⚠️ *SmartNRI Pipeline Alert*\n\n"
        f"*Reason:* {reason}\n\n"
        f"*Last log lines:*\n```\n{log_tail}\n```"
    )
    send_telegram(msg)
    send_email(f"SmartNRI Pipeline Alert: {reason}", f"{reason}\n\n{log_tail}")
    log.warning(f"WATCHDOG ALERT: {reason}")


def run(pipeline_failed: bool = False) -> bool:
    """Returns True if everything is healthy."""
    issues = []

    if pipeline_failed:
        issues.append("Pipeline exited with an error")

    # Check summaries.json exists and is non-empty
    if not SUMMARIES_FILE.exists():
        issues.append("summaries.json does not exist")
    else:
        with open(SUMMARIES_FILE) as f:
            summaries = json.load(f)
        if len(summaries) == 0:
            issues.append("summaries.json is empty — no items published today")

    # Check index.html was updated recently
    if INDEX_HTML.exists():
        mtime = datetime.datetime.fromtimestamp(INDEX_HTML.stat().st_mtime)
        age_hours = (datetime.datetime.now() - mtime).total_seconds() / 3600
        if age_hours > MAX_INDEX_AGE_HOURS:
            issues.append(f"index.html not updated in {age_hours:.0f} hours (max {MAX_INDEX_AGE_HOURS}h)")
    else:
        issues.append("index.html does not exist")

    if issues:
        for issue in issues:
            alert(issue)
        return False

    log.info("Watchdog: all checks passed ✅")
    return True


if __name__ == "__main__":
    run()
