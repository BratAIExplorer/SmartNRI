# SmartNRI — Master Directive (claude.md)
# Layer 1: The Directive

**Version:** 1.0 | **Date:** 21 Feb 2026 | **Phase:** 1 — Malaysia Focus

---

## Project Goal

Build SmartNRI — a fully autonomous, hands-free reference platform for Indian expats living in Malaysia. The platform must verify government rules, detect trending NRI topics, and present clean, mobile-first updates without requiring daily editorial input from the founder. The platform is a **reference guide**, not a financial advisor.

---

## The Golden Rules (Never Break These)

1. **No PII Storage.** Never store, log, or transmit account numbers, passport scans, or personal financial records. Document expiry dates and document *types* only (via dropdown).
2. **No Social Media Scraping.** Do NOT scrape Instagram or YouTube content directly. Use public search APIs and trend-sensing only. Never reproduce a creator's content.
3. **Source-First Publishing.** Every published piece of content MUST have a direct link to a Tier 1 government source. If no government source can be found, mark the item ORANGE (Expert) or flag it as unverified.
4. **Disclaimer on Every Page.** All pages must display: *"SmartNRI is an independent reference guide. Verify with linked official sources before taking action."*
5. **No React, No Databases.** Phase 1 uses static HTML/CSS/JS (Oat UI foundation) + Python scripts for data processing. No complex frameworks. No SQL databases.
6. **Isolated Deployment.** SmartNRI runs in its own Docker container on the VPS. It must NOT share ports, database connections, or environment variables with any other project.
7. **No Hallucination.** If a government source URL returns 404 or the scraper finds no content, the system must NOT generate a summary from memory. It must skip the item and log it.

---

## The Agentic Stack (3 Layers)

### Layer 1 — Directive (Your Job, the Founder)
Define goals in plain English in this file. Update when Phase changes.

### Layer 2 — Orchestration (Claude/Antigravity Job)
Break the directive into sub-tasks. Decide which tools, APIs, and scripts are needed. Handle logic flow.

### Layer 3 — Execution (Agent's Job)
Write Python scripts, run them, test them, fix errors, inject data into the HTML template. Generate Cloudflare Pages or Docker deployment configs.

---

## Phase 1 Scope (Malaysia — Feb–Apr 2026)

### What We Build
- `index.html` — a responsive static site (Oat UI + custom CSS)
- `scraper.py` — fetches updates from Tier 1 government sources
- `summarizer.py` — uses LLM API to generate "So What?" summaries (max 3 bullet points)
- `builder.py` — injects summaries into the HTML template as the daily digest
- `watchdog.py` — health monitor; sends a Telegram/email alert if pipeline fails
- `cron_job.sh` — triggers the full pipeline every 24 hours (GitHub Action or VPS cron)

### What We Do NOT Build in Phase 1
- Community forum
- User accounts or login
- Singapore content
- Native mobile app
- Real-time chatbot (placeholder UI only)

---

## The Data Pipeline

```
[Cron: 24hr] → scraper.py → summarizer.py → builder.py → index.html → Deploy
                    ↓ (on failure)
              watchdog.py → Telegram Alert to Founder
```

### Step 1: Scrape (scraper.py)
Fetch from Tier 1 sources only. Parse HTML or PDF content. Output: raw JSON.

### Step 2: Summarize (summarizer.py)
Send raw JSON to LLM API (OpenAI / Gemini / Claude API). Prompt:
> "You are a compliance guide for Indian expats. Summarize this government update in exactly 3 bullet points. Each bullet is one actionable sentence. Do not add information not present in the source. If unsure, output 'SKIP'."

### Step 3: Build (builder.py)
Inject new content into the HTML template. Replace placeholder card content with today's verified updates. Add the badge (GREEN/ORANGE/BLUE), date, source URL, and "So What?" summary.

### Step 4: Deploy
Commit the updated `index.html` to the deployment branch. Cloudflare Pages auto-deploys, OR the Docker container on the VPS serves the static file via Nginx.

---

## Verification Badge System

| Badge | Label | Criteria |
|---|---|---|
| 🟢 GREEN | Official | Direct link to `.gov.in` or `.gov.my` circular |
| 🟠 ORANGE | Expert | Reputable news or professional advisory (KPMG, ET, law firm) |
| 🔵 BLUE | Community | Trending topic verified against Tier 1 by the AI |
| 🔴 RED | Alert | Urgent, time-sensitive action required |
| ⚪ UNVERIFIED | Flagged | No government source found — display with strong disclaimer |

---

## Tier 1 Source List (Scrape These)

### Malaysia Government
- `https://esd.imi.gov.my` — Employment Pass rules, visa categories
- `https://www.mdec.my` — Digital economy EP applications
- `https://www.hasil.gov.my` — Malaysian tax rules for expats
- `https://www.jpj.gov.my` — Driving license conversion
- `https://www.imi.gov.my` — Visa categories
- `https://www.bnm.gov.my` — Bank Negara financial rules

### India Government
- `https://incometaxindia.gov.in` — ITR, budget FAQs, circulars
- `https://www.rbi.org.in` — Master circulars on NRE/NRO/FEMA
- `https://www.mea.gov.in` — OCI, passport policies
- `https://hcikl.gov.in` — High Commission KL: consular services
- `https://www.sebi.gov.in` — PIS regulations, investment limits
- `https://www.indiabudget.gov.in` — Annual budget documents

### Trend Sensing (API Only — No Content Scraping)
- Google Trends API — NRI-related query monitoring
- YouTube Data API v3 — trending search queries (NOT video content)
- Reddit API — `r/nri`, `r/IndiaInvestments`, `r/india` (questions/topics only)

---

## Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend | HTML + Oat UI + custom CSS | 8KB, zero dependencies, zero build step |
| Automation | Python 3.11 | Simple, well-supported, Claude writes it cleanly |
| LLM | OpenAI API or Gemini API | Configurable via `.env` |
| Deployment | Cloudflare Pages or Nginx on VPS | Zero-cost static hosting |
| Scheduling | Linux cron or GitHub Actions | Hands-free 24hr trigger |
| Monitoring | Watchdog → Telegram Bot | Instant failure alert to founder |
| Secrets | `.env` file (never committed to git) | API keys, Telegram token |

---

## VPS Deployment Rules

- Run in an **isolated Docker container** — do not share network with other projects
- Expose only port `8085` (internal) — proxy via Nginx with a subdomain (e.g., `smartnri.yourdomain.com`)
- Container name: `smartnri_app`
- Volume mount: `/data/smartnri/output/` for generated HTML
- Environment variables loaded from `/data/smartnri/.env` (never hardcode in source)
- Restart policy: `always`

---

## Security Rules

- Never hardcode API keys. Use `.env`.
- Never log user input (checklist responses stay client-side only).
- Run a secret scan before any commit: `grep -r "sk-" .` and `grep -r "AIza" .`
- No admin panel exposed publicly.

---

## Agent Handover Protocol

When your session ends (credits low or task complete), append to `HANDOVER.md`:
```
### Session Handover
- Last Active Agent: [Agent Name + Model]
- Date: [Date]
- Completed: [What was done]
- Where I Left Off: [Exact file, line, or blocker]
- Next Step: [Clear instruction for next agent]
- Critical Context: [VPS port, env var name, or config note]
```

---

## Definition of Phase 1 Done

Phase 1 is complete when:
- [ ] `index.html` auto-updates every 24 hours with 3–5 verified items from Tier 1 sources
- [ ] Each item has the correct badge and a direct source link
- [ ] The watchdog sends an alert if the pipeline breaks
- [ ] The site loads in under 2 seconds on a Malaysian 4G connection
- [ ] The URL is live and shareable in a WhatsApp group
