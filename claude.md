# SmartNRI — Master Directive (claude.md)

# Layer 1: The Directive

**Version:** 2.0 | **Date:** 23 Feb 2026 | **Phase:** 1.5 — Multi-Country Foundation

---

## Vision

> *"Every Indian abroad deserves one place to find the truth — verified, current, and free."*

## Mission

> *"SmartNRI maps the regulatory landscape for Non-Resident Indians across 7+ countries, connecting 18 million NRIs to government-verified intelligence on tax, immigration, banking, and compliance — autonomously, without selling financial products, and without requiring a single human editor."*

## Tagline

> *"The truth before the transaction."*

---

## Core Identity

- **What we are:** The Map — a navigator that finds, verifies, and links NRIs to official government sources. We curate, we don't advise.
- **What we are NOT:** A financial advisor, a services marketplace, a bank, or a source of original legal opinion.
- **Business model:** B2C-first (individual NRIs), B2B-as-a-byproduct (advisors/fintechs find us through traffic).
- **Ambition:** Lifestyle business operations (hands-free, solo founder), positioned as acquisition target by Year 2-3.
- **Language rule:** Never say "you should" or "we recommend." Say "the RBI circular states" and "the MOHRE portal confirms."

---

## Core Values (The 4 Non-Negotiables)

| Value | Meaning | Enforcement |
|---|---|---|
| **Source-First** | No card published without a government source link | Pipeline rejects items without source URLs |
| **Product-Agnostic** | We inform, we don't sell | Affiliate links NEVER inside editorial cards |
| **Privacy-Default** | We store nothing we don't need | No PII beyond name/email/country. Checklists client-side only |
| **Hands-Free** | The platform runs without daily human input | Fully automated pipeline. Founder reviews weekly, not daily |

---

## The Golden Rules (Never Break These)

1. **No PII Storage.** Never store, log, or transmit account numbers, passport scans, or personal financial records. Document expiry dates and document *types* only (via dropdown).
2. **No Social Media Scraping.** Do NOT scrape Instagram or YouTube content directly. Use public search APIs and trend-sensing only. Never reproduce a creator's content.
3. **Source-First Publishing.** Every published piece of content MUST have a direct link to a Tier 1 government source. If no government source can be found, mark the item ORANGE (Expert) or flag it as UNVERIFIED.
4. **Disclaimer on Every Page.** All pages must display: *"SmartNRI is an independent reference guide. Verify with linked official sources before taking action."*
5. **No React, No Databases.** Static HTML/CSS/JS (Oat UI foundation) + Python scripts for data processing. No complex frameworks. No SQL databases. (Review at Phase 4 if scale demands it.)
6. **Isolated Deployment.** SmartNRI runs in its own Docker container on the VPS. It must NOT share ports, database connections, or environment variables with any other project.
7. **No Hallucination.** If a government source URL returns 404 or the scraper finds no content, the system must NOT generate a summary from memory. It must skip the item and log it.
8. **HITL for RED Alerts.** Any RED-badge (urgent/time-sensitive) content MUST be reviewed by the founder before publishing. LLM hallucination on deadlines or penalties could cause real harm. Auto-publish GREEN/ORANGE/BLUE only.
9. **No Financial Advice.** Never cross into investment recommendations, product comparisons, or "you should buy X." Compare RULES across countries; never recommend PRODUCTS. Affiliate links are contextual and clearly labelled, never mixed into editorial cards.
10. **Affiliate Transparency.** All monetization links must be clearly labelled as "Verified Partners" and visually separated from editorial content. Users must always know when a link is commercial.

---

## The Agentic Stack (3 Layers)

### Layer 1 — Directive (Founder's Job)
Define goals in plain English in this file. Update when Phase changes.

### Layer 2 — Orchestration (Claude/Antigravity Job)
Break the directive into sub-tasks. Decide which tools, APIs, and scripts are needed. Handle logic flow.

### Layer 3 — Execution (Agent's Job)
Write Python scripts, run them, test them, fix errors, inject data into the HTML template. Generate deployment configs.

---

## Target Countries (by Phase)

### Phase 1.5 — Multi-Country Foundation (Current)

| Country | NRI Pop | Sources | Status |
|---|---|---|---|
| Malaysia | 185K | ESD/IMI, HASIL, JPJ, BNM, MDEC | Active (Phase 1) |
| USA | 2.07M | IRS, USCIS, State Dept, SSA | Pending |
| Canada | 1.75M | CRA, IRCC, FINTRAC | Pending |
| Singapore | 350K | MOM, IRAS, MAS | Pending |

### Phase 2 — Gulf Expansion

| Country | NRI Pop | Sources | Status |
|---|---|---|---|
| UAE | 3.89M | MOHRE, ICA/ICP, FTA | Planned |
| Saudi Arabia | 2.75M | Qiwa, Absher, MISA, ZATCA | Planned |

### Phase 4+ — Top 20

Kuwait (1.01M), Qatar (835K), Oman (685K), UK (369K), Australia (350K), Bahrain (323K), Germany, Italy, NZ, Philippines, Nepal

### India (GLOBAL — serves all countries)
- `incometaxindia.gov.in` — ITR, budget FAQs, circulars
- `rbi.org.in` — Master circulars on NRE/NRO/FEMA
- `mea.gov.in` — OCI, passport policies
- `sebi.gov.in` — PIS regulations, investment limits
- `indiabudget.gov.in` — Annual budget documents
- Indian Embassy/HC sites per country

---

## The Two-Layer Content Model

| Layer | Scope | Example | Publishing |
|---|---|---|---|
| **GLOBAL** | Affects ALL NRIs | RBI circular, Budget changes, OCI rules, FEMA | Write once, serve on every country feed |
| **LOCAL** | Affects NRIs in THAT country | UAE golden visa, US FBAR deadline, Canada PR tax | Country-specific feed only |

~40% of content is GLOBAL. Adding a new country only requires the LOCAL layer.

---

## The 4-Tab Structure

| Tab | Content | Monetization |
|---|---|---|
| **Signal** | Daily verified updates with country filter | Contextual affiliate links below relevant cards |
| **Guides** | Transition checklists, compliance calendars, self-audit | Paid Starter Kits ($29-49), affiliate links |
| **Compare** | Regulatory comparison tables across countries (tax, banking, investments, insurance) | Affiliate links to tax/remittance services |
| **Ask** | User questions → AI-verified answers with source links | Pro tier for priority answers |

---

## The Data Pipeline

### Current Architecture (Phase 1–1.5)

```
[Cron: 24hr] → scraper.py → summarizer.py → publisher.py → per-country HTML → Deploy
                    ↓ (on failure)
              watchdog.py → Telegram Alert to Founder
```

### Target Architecture (Phase 3+)

```
Trend Sensor → topics → Search Discoverer → candidates →
Source Scraper → verified items → Summarizer → Publisher (per-country)
                                      ↓ RED items
                              Founder Review (HITL) → Publish or Reject
```

### Pipeline Steps

**Step 1: Scrape** — Fetch from country profile sources. Output: per-country `raw_content.json`.

**Step 2: Summarize** — LLM generates structured JSON with badge, bullets, "So What?" summary. Temperature 0.1. If unsure, output `{"skip": true}`.

**Step 3: Publish** — Inject cards into per-country HTML pages. Update date. Send Telegram alerts for RED items (after founder review).

**Step 4: Deploy** — Commit updated HTML. Cloudflare Pages or Nginx serves static files.

---

## Country Profile System

Each country is a JSON profile in `countries/`. Adding a country = adding a JSON file.

```json
{
  "country_code": "AE",
  "display_name": "UAE",
  "flag_emoji": "...",
  "timezone": "Asia/Dubai",
  "languages": ["en", "ar"],
  "sources": [...],
  "search_queries": [...],
  "compliance_calendar": [...]
}
```

Pipeline reads profiles → scrapes per-country → summarizes per-country → publishes per-country HTML.

---

## Verification Badge System

| Badge | Label | Criteria | Gov Domain Examples |
|---|---|---|---|
| GREEN | Official | Direct link to government circular | `.gov.in`, `.gov.my`, `.gov.ae`, `.gov.sa`, `.gov`, `.gc.ca`, `.gov.sg` |
| ORANGE | Expert | Reputable advisory (Big4, ET, law firm) | KPMG, Deloitte, Economic Times |
| BLUE | Community | Trending topic verified against Tier 1 | Reddit question + gov confirmation |
| RED | Alert | Urgent, time-sensitive (deadline < 30 days). **Requires HITL review.** | Any source, but must be verified |
| UNVERIFIED | Flagged | No government source found | Display with strong disclaimer |

---

## Monetization Principles

### What We DO
1. **Contextual Affiliate Partners** — verified partners embedded below relevant content, clearly labelled
2. **Country Starter Kits** ($29-49) — paid digital products for NRI transitions
3. **SmartNRI Pro** ($5/month) — WhatsApp/email digest, early alerts, priority Ask
4. **Sponsored Verified Cards** (Phase 4+) — B2B partners pay for verified sponsored content

### What We NEVER DO
- Gate content behind a paywall (all information stays free)
- Recommend specific financial products
- Place affiliate links inside editorial cards
- Run banner ads or AdSense
- Build our own fintech/banking product
- Give investment, tax, or legal advice

---

## Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend | HTML + Oat UI + custom CSS | 8KB, zero dependencies, zero build step |
| Automation | Python 3.11 | Simple, well-supported |
| LLM | Gemini API (primary) / OpenAI API (fallback) | Configurable via `.env` |
| Deployment | Cloudflare Pages or Nginx on VPS | Zero-cost static hosting |
| Scheduling | Linux cron or GitHub Actions | Hands-free 24hr trigger |
| Monitoring | Watchdog → Telegram Bot | Instant failure alert to founder |
| Secrets | `.env` file (never committed to git) | API keys, tokens |

---

## VPS Deployment Rules

- Run in an **isolated Docker container** — do not share network with other projects
- Expose only port `8085` (internal) — proxy via Nginx with subdomain
- Container name: `smartnri_app`
- Volume mount: `/data/smartnri/output/` for generated HTML
- Environment variables from `/data/smartnri/.env` (never hardcode)
- Restart policy: `always`

---

## Security Rules

- Never hardcode API keys. Use `.env`.
- Never log user input (checklist responses stay client-side only).
- Run a secret scan before any commit: `grep -r "sk-" .` and `grep -r "AIza" .`
- No admin panel exposed publicly.
- Pin all Python package versions in `requirements.txt`.
- Affiliate disclosure on every page with partner links.

---

## Content Strategy

- **Quality over velocity.** 1 deeply researched, perfectly verified article per week > 5 shallow daily items. Depth builds trust; volume builds noise.
- **Gulf vs Western segmentation.** Gulf NRIs care about labour law, iqama, exit visas. Western NRIs care about FATCA, FBAR, estate planning. Content must reflect this.
- **WhatsApp-first distribution.** Website is the content engine; WhatsApp is the distribution engine. 85% open rates for Gulf NRIs.
- **SEO as long-term moat.** Evergreen guides target high-search queries: "moving to UAE from India," "FBAR deadline NRI," "returning to India checklist."
- **Cold start plan.** First 100 users from founder's personal network + one viral guide shared in NRI WhatsApp groups.

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

## Key Reference Documents

| Document | Purpose |
|---|---|
| `specs/requirements.md` | Full product features (v2.0) — tabs, country profiles, engines, monetization |
| `specs/backlog.md` | Product backlog — epics, stories, priorities, sprint plan |
| `specs/architecture.md` | System architecture — pipeline, deployment, security |
| `specs/session_dialogues/` | Living record of founder-AI strategic dialogues |
| `state/system_state.json` | Machine-readable roadmap state tracker |
| `HANDOVER.md` | Agent session handover log |
| `HANDOVER_PROTOCOL.md` | Handover rules and templates |

---

## Definition of Done (Current Phase: 1.5)

Phase 1.5 is complete when:
- [ ] Country profile schema defined and implemented (`countries/` directory)
- [ ] USA, Canada, Singapore sources added and scraping
- [ ] Pipeline produces per-country output files (global + local separation)
- [ ] Frontend country switcher working (dropdown + URL routing)
- [ ] Pipeline runs end-to-end for 4 countries (MY + US + CA + SG)
- [ ] Each item has correct badge and direct source link
- [ ] The watchdog alerts if any country's pipeline fails
- [ ] Site loads under 2 seconds on 4G
- [ ] URL is shareable per-country in WhatsApp groups
