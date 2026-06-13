# SmartNRI — System Architecture

**Version:** 2.0 | **Phase:** 1.5 (Multi-Country Foundation) | **Date:** 23 Feb 2026

---

## System Overview

SmartNRI is a **static-site-first** autonomous publishing system serving NRIs across 7+ countries. The frontend is pure HTML/CSS/JS — one template generates per-country static pages. The automation layer (Python scripts) runs on a schedule, fetches government data from country profiles, summarizes it with an LLM, and publishes per-country HTML pages.

There is no application server. There is no database. There is no user authentication (registration is localStorage-only).

---

## High-Level Architecture Diagram

### Current (Phase 1.5)

```
┌─────────────────────────────────────────────────────────────┐
│                      VPS / Cron (24hr)                      │
│                                                             │
│  ┌─────────────┐                                            │
│  │  countries/  │ ← JSON profiles (my.json, us.json, ...)   │
│  │  global-in   │                                            │
│  └──────┬──────┘                                            │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  scraper.py  │───▶│summarizer.py │───▶│ publisher.py │   │
│  │ (per-country)│    │  (LLM API)   │    │(per-country) │   │
│  └──────┬───────┘    └──────────────┘    └──────┬───────┘   │
│         │                                       │           │
│  Tier 1 Gov Sites                    ┌──────────┴────────┐  │
│  (per country profile)               │  Per-Country HTML  │  │
│                                      │  my.html, us.html  │  │
│                                      │  ca.html, sg.html  │  │
│                                      │  index.html (hub)  │  │
│                                      └──────────┬────────┘  │
│                                                 │           │
│                                      ┌──────────▼────────┐  │
│                                      │  Deploy: Nginx /  │  │
│                                      │  Cloudflare Pages  │  │
│                                      └───────────────────┘  │
│                                                             │
│  ┌──────────────┐                                           │
│  │ watchdog.py  │───▶ Telegram/Email Alert (on fail)        │
│  │(per-country) │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Target (Phase 3+)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌───────────────┐                                          │
│  │ Trend Sensor  │ ← Google Trends, Reddit, YouTube API    │
│  └───────┬───────┘                                          │
│          ▼ topics                                            │
│  ┌───────────────┐                                          │
│  │   Search      │ ← Google Custom Search / News API       │
│  │  Discoverer   │                                          │
│  └───────┬───────┘                                          │
│          ▼ candidates                                        │
│  ┌───────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Source Scraper │───▶│  Summarizer  │───▶│  Publisher   │  │
│  │ (per-country) │    │ (LLM + Critic│    │(per-country) │  │
│  └───────────────┘    │  + Verifier) │    └──────────────┘  │
│                       └──────┬───────┘                      │
│                              │ RED items                     │
│                       ┌──────▼───────┐                      │
│                       │ Founder HITL │ ← Sunday batch review│
│                       │ (approve/    │                      │
│                       │  reject)     │                      │
│                       └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

---

## The Two-Layer Content Model

| Layer | Scope | Data Location | Publishing |
|---|---|---|---|
| **GLOBAL** (India-side) | Affects ALL NRIs | `data/global/` | Appears on every country page |
| **LOCAL** (Host-country) | Affects NRIs in THAT country | `data/countries/{code}/` | Country-specific page only |

~40% of content is GLOBAL. Adding a new country only requires the LOCAL layer.

---

## Country Profile System

Each supported country is defined as a JSON profile in `countries/`. Adding a country = adding a JSON file. No code changes required.

### Profile Schema

```json
{
  "country_code": "AE",
  "display_name": "UAE",
  "flag_emoji": "...",
  "timezone": "Asia/Dubai",
  "languages": ["en", "ar"],
  "currency": "AED",
  "scope": "local",
  "topics": ["visa", "labour_law", "tax", "banking", "driving", "property"],
  "sources": [
    {
      "id": "mohre",
      "name": "Ministry of Human Resources (MOHRE)",
      "url": "https://www.mohre.gov.ae/en/...",
      "scrape_method": "html",
      "tier": 1,
      "badge": "GREEN",
      "selectors": { "title": "h3.news-title", "body": "div.news-body" },
      "active": true
    }
  ],
  "search_queries": [
    "UAE visa rules Indian workers 2026",
    "golden visa India eligibility"
  ],
  "compliance_calendar": [
    { "month": 3, "day": 31, "event": "UAE corporate tax return deadline", "source": "https://tax.gov.ae/..." }
  ]
}
```

### Profile: India GLOBAL (`countries/global-in.json`)

Special profile with `"scope": "global"` — sources serve ALL country feeds.

Sources:
- `incometaxindia.gov.in` — ITR, budget, circulars
- `rbi.org.in` — NRE/NRO/FEMA master circulars (HTML + RSS)
- `mea.gov.in` — OCI, passport policies
- `sebi.gov.in` — PIS regulations, investment limits
- `indiabudget.gov.in` — Annual budget documents
- `passportindia.gov.in` — Passport Seva

### Country Profiles (Phase 1.5)

| Profile | File | Status | Key Sources |
|---|---|---|---|
| India (GLOBAL) | `countries/global-in.json` | Pending | RBI, Income Tax, SEBI, MEA, Passport Seva |
| Malaysia | `countries/my.json` | Pending (migrate from `sources.json`) | ESD/IMI, HASIL, JPJ, BNM |
| USA | `countries/us.json` | Pending | IRS, USCIS, State Dept, SSA |
| Canada | `countries/ca.json` | Pending | CRA, IRCC, FINTRAC |
| Singapore | `countries/sg.json` | Pending | MOM, IRAS, MAS |

### Country Profiles (Phase 2)

| Profile | File | Status | Key Sources |
|---|---|---|---|
| UAE | `countries/ae.json` | Planned | MOHRE, ICA/ICP, FTA |
| Saudi Arabia | `countries/sa.json` | Planned | Qiwa, Absher, MISA, ZATCA |

---

## Component Breakdown

### 1. Profile Loader (`pipeline/profile_loader.py`) — NEW

- **Purpose:** Load all active country profiles, merge GLOBAL sources with LOCAL sources per country
- **Input:** `countries/*.json`
- **Output:** Combined source list per country for scraper consumption
- **Rules:**
  - Only load profiles with `"active": true` at the profile level
  - Only load sources with `"active": true` within each profile
  - GLOBAL sources appear in every country's source list

### 2. `scraper.py` — Data Fetcher (Refactored)

- **Purpose:** Fetch raw content from Tier 1 government sources, per country
- **Method:** `requests` + `BeautifulSoup` for HTML; `feedparser` for RSS; `PyMuPDF` for PDFs
- **Input:** Country profiles via profile loader
- **Output:** Per-country raw files:
  - `data/global/raw_content.json` (India GLOBAL sources)
  - `data/countries/{code}/raw_content.json` (per-country LOCAL sources)
- **Rules:**
  - Iterate over country profiles from loader
  - Separate GLOBAL output from LOCAL output
  - If URL returns 404 → log and skip (Golden Rule #7)
  - Content hash deduplication across runs
  - Max 5 items per country per run
  - 1-second polite delay between requests
  - Per-domain rate limiting (configurable)

```python
# Output schema (per-country raw_content.json)
[
  {
    "id": "mohre-golden-visa-2026-02-23",
    "source_id": "mohre",
    "source_name": "Ministry of Human Resources (MOHRE)",
    "source_url": "https://www.mohre.gov.ae/...",
    "domain": "mohre.gov.ae",
    "tier": 1,
    "badge": "GREEN",
    "scope": "local",
    "country_code": "AE",
    "topics": ["visa", "labour_law"],
    "title": "Golden Visa Eligibility Update",
    "raw_text": "...",
    "date_found": "2026-02-23",
    "content_hash": "sha256:abc123"
  }
]
```

### 3. `summarizer.py` — LLM Processor (Enhanced)

- **Purpose:** Transform raw government text into badge-tagged bullet-point summaries
- **Method:** LLM API call (Gemini `gemini-flash-latest` primary, OpenAI `gpt-4o-mini` fallback)
- **Input:** Per-country `raw_content.json` files
- **Output:** Per-country `summaries.json` files
- **Temperature:** 0.1 (factual, not creative)

**Verification Layers (phased):**

| Layer | Phase | Function |
|---|---|---|
| Executor | 1.5 (now) | Generate summary from raw content |
| Verifier | 1.5 (now) | Check source URL returns HTTP 200. If 404 → skip |
| Critic | 2+ | Second LLM pass: check every claim maps to source text |

**Source Match Validation (automated — no human needed for non-RED):**
1. Summarizer extracts a supporting quote from raw source text
2. Verifier checks: URL returns 200 + quote exists in raw text + no hallucinated claims
3. All checks pass + non-RED badge → AUTO-PUBLISH
4. Any check fails → QUARANTINE (`data/staging/pending_review.json`)
5. RED badge → ALWAYS QUARANTINE → Telegram to founder → "OK"/"NO" reply → 48hr auto-publish fallback with disclaimer

**Founder effort:** ~15 min/week (Phase 1.5-2), ~5 min/week (Phase 3+)

```python
# Output schema (per-country summaries.json)
[
  {
    "id": "mohre-golden-visa-2026-02-23",
    "source_id": "mohre",
    "source_name": "Ministry of Human Resources (MOHRE)",
    "source_url": "https://www.mohre.gov.ae/...",
    "domain": "mohre.gov.ae",
    "tier": 1,
    "scope": "local",
    "country_code": "AE",
    "date": "2026-02-23",
    "badge": "GREEN",
    "title": "UAE Expands Golden Visa to Skilled Tech Workers",
    "so_what": "Indian IT professionals in UAE may now qualify for 10-year residency without employer sponsorship.",
    "bullets": [
      "Check eligibility under the new 'Specialized Talent' category on ICP portal.",
      "Ensure your salary certificate and education attestation are current.",
      "Apply directly via ICP website — no employer nomination required."
    ],
    "skip": false
  }
]
```

### 4. `publisher.py` — Multi-Page Publisher (Refactored)

- **Purpose:** Generate per-country HTML pages from summaries
- **Input:** Per-country `summaries.json` + `data/global/summaries.json` + `templates/index_template.html`
- **Output:** Per-country HTML files in `frontend/`:
  - `frontend/index.html` — Landing page with country picker
  - `frontend/my.html` — Malaysia feed (GLOBAL + MY local)
  - `frontend/us.html` — USA feed (GLOBAL + US local)
  - `frontend/ca.html` — Canada feed
  - `frontend/sg.html` — Singapore feed
  - (Phase 2: `frontend/ae.html`, `frontend/sa.html`)
- **Rules:**
  - Each country page shows GLOBAL cards + that country's LOCAL cards
  - GLOBAL cards have subtle "Applies to all NRIs" indicator
  - Cards sorted by date, then badge priority (RED > GREEN > ORANGE > BLUE)
  - Inject max 5 cards per country page
  - Update date header per country page
  - Telegram alerts for RED items sent to founder (HITL review)
  - Weekly digest pushed via Telegram (all countries summary)

### 5. `watchdog.py` — Health Monitor (Enhanced)

- **Purpose:** Detect pipeline failures per country, alert founder
- **Trigger:** Called at end of each pipeline run
- **Alert conditions:**
  - Any country's scraper returns zero items for 3+ consecutive days
  - Any country's `summaries.json` is empty
  - Any country's HTML page not modified in 28+ hours
  - Pipeline exits with non-zero code
- **Alert method:** Telegram Bot + email fallback
- **Alert payload:** Country code + which step failed + last 15 lines of log

### 6. `main.py` — Pipeline Orchestrator (Updated)

- **Purpose:** Run the full pipeline across all countries
- **Sequence:** Load profiles → Scrape all → Summarize all → Publish all → Watchdog
- **Flags:**
  - `--dry-run` — scrape only, no publishing
  - `--country {code}` — run for single country (for testing)

### 7. `cron_job.sh` / GitHub Actions — Scheduler

- **Schedule:** Daily at 06:00 MYT (22:00 UTC previous day)
- **Method:** GitHub Actions workflow (`.github/workflows/daily_update.yml`) or VPS cron
- **Workflow:** Run `main.py` → commit updated HTML → deploy

---

## Data Directory Structure

```
data/
├── global/
│   ├── raw_content.json          ← India-side GLOBAL items
│   └── summaries.json
├── countries/
│   ├── my/
│   │   ├── raw_content.json      ← Malaysia LOCAL items
│   │   └── summaries.json
│   ├── us/
│   │   ├── raw_content.json
│   │   └── summaries.json
│   ├── ca/
│   │   ├── raw_content.json
│   │   └── summaries.json
│   └── sg/
│       ├── raw_content.json
│       └── summaries.json
├── staging/                       ← Items awaiting founder review
│   └── pending_review.json
├── content_hashes.json            ← Deduplication cache
└── trends.json                    ← Trend sensor output (Phase 3)

countries/                          ← Country profile definitions
├── global-in.json
├── my.json
├── us.json
├── ca.json
├── sg.json
├── ae.json                        ← Phase 2
└── sa.json                        ← Phase 2

frontend/
├── index.html                     ← Landing page + country picker
├── my.html                        ← Malaysia feed (generated)
├── us.html                        ← USA feed (generated)
├── ca.html                        ← Canada feed (generated)
├── sg.html                        ← Singapore feed (generated)
└── guides/                        ← Phase 2: guide pages
    └── return-to-india.html

templates/
└── index_template.html            ← Master template

pipeline/
├── main.py                        ← Orchestrator
├── scraper.py                     ← Data fetcher
├── summarizer.py                  ← LLM processor
├── publisher.py                   ← HTML generator
├── watchdog.py                    ← Health monitor
├── profile_loader.py              ← NEW: country profile loader
├── sources.json                   ← DEPRECATED: replaced by countries/*.json
└── tests/
    ├── test_scraper.py
    ├── test_summarizer.py
    └── test_adversarial.py        ← Phase 2: adversarial testing
```

---

## Frontend Architecture

### Framework
- **Base:** Oat UI (8KB, zero dependencies)
- **Custom CSS:** `style_smartnri.css` (~5KB) — badge system, card layout, brand colours
- **No JS Framework:** Vanilla JS only for tab switching, country selector, checklist interaction
- **Fonts:** Inter via Google Fonts (loaded async)

### 4-Tab Structure

| Tab | Content | Data Source |
|---|---|---|
| **Signal** | Daily verified updates with country filter | Per-country `summaries.json` + GLOBAL |
| **Guides** | Transition checklists, compliance calendars | `guides/*.json` (Phase 2) |
| **Compare** | Regulatory comparison tables | `compare/*.json` (Phase 2) |
| **Ask** | User questions → verified answers | Placeholder (Phase 1.5), functional (Phase 3) |

### Country Switcher
- Dropdown at top of Signal tab
- Options: All countries with active profiles + "All"
- Persists selection in localStorage (`snri_country` key)
- Each country has a bookmarkable URL: `/us.html`, `/my.html`, etc.

### Registration Gate (Existing)
- Full-screen modal on first visit
- Fields: Name, Email, Country of Residence, Role
- Storage: `localStorage` key `snri_user`
- Signal tab ungated (teaser). Guides/Compare/Ask gated
- Backend hook ready: `fetch('/api/register', ...)`

---

## VPS Deployment Architecture

### Isolation Rules (CRITICAL)
- SmartNRI runs in its own Docker container. **No shared networks with other projects.**
- Container name: `smartnri_app`
- Internal port: `8085`
- External access: Via Nginx reverse proxy on subdomain
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

## Secrets Management

```env
# .env.template
LLM_PROVIDER=gemini
OPENAI_API_KEY=
GEMINI_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
ALERT_EMAIL=
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=noreply@smartnri.com
YOUTUBE_API_KEY=
```

**Rules:**
- Never commit `.env` to Git
- Keys loaded at runtime from `/data/smartnri/.env`
- Rotate keys every 90 days
- Pre-commit secret scan: `grep -r "sk-" .` and `grep -r "AIza" .`

---

## Security Architecture

| Threat | Mitigation |
|---|---|
| Hardcoded secrets | `.env` only, pre-commit secret scan |
| Scraped PII | No user data stored server-side; checklists client-side only |
| Container escape | Isolated Docker network `smartnri_isolated` |
| LLM hallucination | `{"skip": true}` protocol; source URL liveness check; HITL for RED items; Critic pass (Phase 2+) |
| Dependency attack | Pin all Python package versions in `requirements.txt` |
| Cross-project interference | No shared volumes, ports, or networks with other VPS projects |
| Affiliate trust erosion | Partner links NEVER inside editorial cards. Clear "Verified Partners" label |
| Stale content | Source URL liveness check in summarizer. Content freshness date on every card |

---

## Monitoring & Logging

| Log | Location | Retention |
|---|---|---|
| Pipeline run log | `logs/pipeline.log` | 30 days rolling |
| Scraper errors | `logs/scraper_errors.log` | 7 days |
| LLM API responses | `logs/llm_audit.log` | 7 days |
| Successful deploys | `logs/deploy.log` | 90 days |
| Watchdog alerts | `logs/watchdog.log` | 30 days |

---

## Phase 3+ Architecture (Future Reference)

| Component | Technology | Phase |
|---|---|---|
| Search Discoverer | Google Custom Search API + LLM classifier | Phase 3 |
| Trend Sensor | Google Trends API + Reddit API + YouTube Data API | Phase 3 |
| SmartNRI Pro delivery | WhatsApp Business API + SendGrid email | Phase 3 |
| Ask Tab (functional) | LLM Q&A pipeline with source verification | Phase 3 |
| Enterprise API | FastAPI REST service with API key auth | Phase 4 |
| Sponsored Cards | Submission portal + AI verification + billing | Phase 4 |
| Multilingual alerts | LLM translation (Hindi + Malayalam) for RED cards | Phase 2+ |

---

## Government API Preferences

Where available, prefer structured APIs over HTML scraping:

| Country | API Source | Advantage |
|---|---|---|
| USA | `api.data.gov` | Structured, stable, no HTML breakage |
| UAE | `api.government.ae` | Official API marketplace |
| Saudi Arabia | `dga.gov.sa` (RAQMI) | Government-endorsed |
| India | RSS feeds (RBI, Income Tax) | Structured, reliable |

Migrate from HTML scraping to APIs as they become available and approved. Don't block on API registration — scrape first, migrate later.
