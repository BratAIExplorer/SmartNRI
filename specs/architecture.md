# SmartNRI — System Architecture

**Version:** 1.0 | **Phase:** 1 (Malaysia) | **Date:** 21 Feb 2026

---

## System Overview

SmartNRI is a **static-site-first** autonomous publishing system. The frontend is a pure HTML/CSS/JS page. The automation layer (Python scripts) runs on a schedule, fetches government data, summarizes it with an LLM, and injects the result into the static HTML template before deploying it.

There is no application server. There is no database. There is no user authentication.

---

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                   VPS / Cron                    │
│                                                 │
│  ┌──────────┐    ┌─────────────┐    ┌────────┐  │
│  │scraper.py│───▶│summarizer.py│───▶│builder │  │
│  │ (Fetch)  │    │ (LLM API)   │    │  .py   │  │
│  └────┬─────┘    └─────────────┘    └───┬────┘  │
│       │                                 │       │
│  Tier 1 Gov Sites              index.html       │
│  (esd.imi.gov.my,              (updated)        │
│   incometaxindia.gov.in, ...)       │           │
│                                      │           │
│                              ┌───────▼───────┐  │
│                              │  Deploy to    │  │
│                              │  Cloudflare   │  │
│                              │  Pages / Nginx│  │
│                              └───────────────┘  │
│                                                 │
│  ┌──────────────┐                               │
│  │ watchdog.py  │───▶ Telegram Alert (on fail)  │
│  └──────────────┘                               │
└─────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. `scraper.py` — Data Fetcher
- **Purpose:** Fetch raw content from Tier 1 government sources
- **Method:** `requests` + `BeautifulSoup` for HTML pages; `PyMuPDF` or `pdfplumber` for PDF circulars
- **Output:** `raw_content.json` — array of `{source_url, title, raw_text, date_found, tier}`
- **Rules:**
  - Only fetch from the 13 whitelisted Tier 1 domains in `claude.md`
  - If a URL returns 404 → log to `pipeline.log` and skip
  - If content unchanged since last run → skip (compare hash)
  - Max 5 items per run to avoid noise

```python
# Output schema (raw_content.json)
[
  {
    "id": "ep-salary-2026-02-21",
    "source_url": "https://esd.imi.gov.my/...",
    "title": "Employment Pass Salary Threshold Update",
    "raw_text": "...",
    "date_found": "2026-02-21",
    "tier": 1,
    "content_hash": "sha256:abc123"
  }
]
```

### 2. `summarizer.py` — LLM Processor
- **Purpose:** Transform raw government text into 3-bullet "So What?" summaries
- **Method:** LLM API call (configurable: OpenAI `gpt-4o-mini` or Gemini `gemini-1.5-flash`)
- **Input:** `raw_content.json`
- **Output:** `summaries.json`
- **Prompt Template:**
  ```
  You are a compliance guide for Indian expats. 
  Summarize the following government update in exactly 3 bullet points.
  Each bullet is one actionable sentence. 
  Start each bullet with a verb (e.g. "Review", "Convert", "File").
  Do not add information not present in the source. 
  If you cannot summarize accurately, output: {"skip": true}.
  
  Source: {source_url}
  Content: {raw_text}
  ```
- **Rules:**
  - If LLM returns `{"skip": true}` → log and skip that item
  - If API call fails → watchdog alert, abort run
  - Temperature: 0.1 (factual, not creative)

```python
# Output schema (summaries.json)
[
  {
    "id": "ep-salary-2026-02-21",
    "badge": "GREEN",
    "title": "Malaysia EP Salaries Double from June 2026",
    "so_what": "The minimum salary for Category I Employment Pass jumps to RM20,000/month.",
    "bullets": [
      "Check your current EP category against the new thresholds before June 1.",
      "Succession planning documentation is now mandatory for Cat II and III holders.",
      "New ePASS digital system replaces sticker-based permits for renewals."
    ],
    "source_url": "https://esd.imi.gov.my/...",
    "date": "2026-02-21",
    "skip": false
  }
]
```

### 3. `builder.py` — HTML Injector
- **Purpose:** Write the day's summaries into the `index.html` template
- **Method:** String replacement into clearly marked template slots
- **Input:** `summaries.json` + `index_template.html`
- **Output:** `index.html` (the live file served to users)
- **Rules:**
  - Never modify CSS or JS — only the content slots
  - Inject max 5 cards; if fewer summaries exist, use last-cached content to fill
  - Update the date header automatically

### 4. `watchdog.py` — Health Monitor
- **Purpose:** Detect pipeline failures and alert the founder
- **Trigger:** Called at end of each pipeline run
- **Alert conditions:**
  - Any script exits with non-zero code
  - `summaries.json` is empty
  - `index.html` was not modified in last 28 hours
- **Alert method:** Telegram Bot API (configurable) or email via SMTP
- **Alert payload:** Timestamp + which step failed + last 10 lines of `pipeline.log`

### 5. `cron_job.sh` — Scheduler
- **Purpose:** Run the full pipeline every 24 hours automatically
- **Schedule:** 06:00 MYT daily (22:00 UTC previous day)
- **Method:** Linux cron on VPS or GitHub Actions workflow (`.github/workflows/daily_update.yml`)

---

## Frontend Architecture

### Framework
- **Base:** [Oat UI](https://oat.ink) (8KB, zero dependencies)
- **Custom CSS:** `style_smartnri.css` (~5KB) — badge system, card layout, brand colours
- **No JS Framework:** Vanilla JS only for tab switching and checklist interaction
- **Fonts:** Inter via Google Fonts (loaded async)

### File Structure (Frontend)
```
/SmartNRI
├── index.html              ← Auto-generated daily by builder.py
├── index_template.html     ← Master template (never auto-overwritten)
├── style_smartnri.css      ← Custom brand styles (Oat + SmartNRI)
└── assets/
    └── logo.svg
```

### Content Injection Slots (in index_template.html)
```html
<!-- {{CONTENT_DATE}} -->        ← Today's date
<!-- {{CARD_1}} -->              ← First update card
<!-- {{CARD_2}} -->              ← Second update card
...
<!-- {{CARD_5}} -->              ← Fifth update card
```

---

## VPS Deployment Architecture

### Isolation Rules (CRITICAL)
- SmartNRI runs in its own Docker container. **No shared networks with other projects.**
- Container name: `smartnri_app`
- Internal port: `8085`
- External access: Via Nginx reverse proxy on subdomain (e.g., `smartnri.yourdomain.com`)
- Restart policy: `always`

### Docker Configuration
```yaml
# docker-compose.yml
version: '3.8'
services:
  smartnri_app:
    build: .
    container_name: smartnri_app
    restart: always
    ports:
      - "8085:80"
    volumes:
      - /data/smartnri/output:/usr/share/nginx/html:ro
      - /data/smartnri/.env:/app/.env:ro
    networks:
      - smartnri_network

networks:
  smartnri_network:
    driver: bridge
    name: smartnri_isolated
```

### Nginx Config (Reverse Proxy)
```nginx
server {
    listen 443 ssl;
    server_name smartnri.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8085;
    }
}
```

---

## Secrets Management (`.env.template`)

```env
# LLM API (choose one, configure in summarizer.py)
OPENAI_API_KEY=
GEMINI_API_KEY=

# Watchdog Alert
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Optional: SMTP alert fallback
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASS=
ALERT_EMAIL=
```

**Rules:**
- Never commit `.env` to Git. `.gitignore` must include `.env`
- Keys are loaded at runtime from `/data/smartnri/.env`
- Rotate keys every 90 days

---

## Security Architecture

| Threat | Mitigation |
|---|---|
| Hardcoded secrets | `.env` only, pre-commit secret scan |
| Scraped PII | No user data stored server-side; checklists client-side only |
| Container escape | Isolated Docker network `smartnri_isolated` |
| LLM hallucination | `{"skip": true}` protocol; mandatory source URL on every card |
| Dependency attack | Pin all Python package versions in `requirements.txt` |
| Cross-project interference | No shared volumes, ports, or networks with other VPS projects |

---

## Monitoring & Logging

| Log | Location | Retention |
|---|---|---|
| Pipeline run log | `/data/smartnri/logs/pipeline.log` | 30 days rolling |
| Scraper errors | `/data/smartnri/logs/scraper_errors.log` | 7 days |
| LLM API responses | `/data/smartnri/logs/llm_audit.log` | 7 days |
| Successful deploys | `/data/smartnri/logs/deploy.log` | 90 days |

---

## Phase 2+ Architecture (Future Reference)

| Feature | Technology |
|---|---|
| Real-time chatbot | FastAPI backend + LLM with RAG over Tier 1 sources |
| Singapore content | New scraper module, same pipeline |
| User notifications | Cloudflare Workers + KV store |
| Community forum | Lightweight Discourse or custom Flask app |
| Premium scorecard | Stateless personalisation via URL query params |
