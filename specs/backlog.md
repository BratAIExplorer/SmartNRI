# SmartNRI — Product Backlog

**Version:** 1.0 | **Date:** 23 Feb 2026 | **Owner:** Founder + AI Agents

> Prioritised using MoSCoW (Must/Should/Could/Won't) within each phase.
> Story points are T-shirt sizes: S (1-2 days), M (3-5 days), L (1-2 weeks), XL (2-4 weeks).

---

## Phase 1.5 — Multi-Country Foundation

**Goal:** Refactor from Malaysia-only to a multi-country architecture. Launch USA, Canada, Singapore alongside Malaysia. Establish the global vs local content split.

**Target:** March 2026

### Epic 1.5.1: Country Profile System

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 1.5.1.1 | Define country profile JSON schema | Must | S | Schema supports: country_code, display_name, flag, timezone, languages, sources[], search_queries[], compliance_calendar[]. Documented in specs/. |
| 1.5.1.2 | Create country profile: Malaysia (migrate from flat sources.json) | Must | S | Existing Malaysia sources migrated to `countries/my.json`. Pipeline still works with new structure. |
| 1.5.1.3 | Create country profile: USA | Must | M | `countries/us.json` with IRS, USCIS, State Dept sources. At least 4 active sources. Scraper fetches successfully. |
| 1.5.1.4 | Create country profile: Canada | Must | M | `countries/ca.json` with CRA, IRCC sources. At least 3 active sources. RSS feeds preferred where available. |
| 1.5.1.5 | Create country profile: Singapore | Must | M | `countries/sg.json` with MOM, IRAS, MAS sources. At least 3 active sources. |
| 1.5.1.6 | Create country profile: India (GLOBAL) | Must | M | `countries/global-in.json` with RBI, SEBI, Income Tax, MEA, Passport Seva. These sources serve ALL country feeds. |
| 1.5.1.7 | Build profile loader utility | Must | S | Python utility that loads all active country profiles, merges GLOBAL sources with LOCAL sources per country. Used by scraper. |

### Epic 1.5.2: Pipeline Multi-Country Refactor

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 1.5.2.1 | Refactor scraper.py to iterate over country profiles | Must | M | Scraper loads country profiles via loader. Outputs per-country raw files: `data/countries/{code}/raw_content.json`. GLOBAL items output to `data/global/raw_content.json`. |
| 1.5.2.2 | Refactor summarizer.py for per-country processing | Must | M | Summarizer processes each country's raw file independently. Outputs `data/countries/{code}/summaries.json` + `data/global/summaries.json`. |
| 1.5.2.3 | Refactor publisher.py for multi-page output | Must | L | Publisher generates `frontend/{code}.html` for each country (e.g., `us.html`, `ca.html`). Each page includes GLOBAL cards + that country's LOCAL cards. Landing page (`index.html`) has country picker. |
| 1.5.2.4 | Update main.py orchestrator | Must | S | Main pipeline iterates: scrape all → summarize all → publish all → watchdog. Single cron trigger handles all countries. |
| 1.5.2.5 | Update watchdog.py for multi-country health checks | Should | S | Watchdog checks each country's summaries + HTML staleness. Alert specifies which country's pipeline failed. |
| 1.5.2.6 | Add `--country` flag to main.py | Should | S | `python main.py --country us` runs pipeline for a single country. Useful for testing and debugging. |

### Epic 1.5.3: Frontend Country Switcher

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 1.5.3.1 | Add country selector dropdown to Signal tab | Must | M | Dropdown at top of feed. Options: USA, Canada, Singapore, Malaysia, "All". Persists selection in localStorage. |
| 1.5.3.2 | Generate per-country static HTML pages | Must | M | Publisher generates `us.html`, `ca.html`, `sg.html`, `my.html`. Each contains global + local cards. URL-shareable: `smartnri.com/us`. |
| 1.5.3.3 | Update landing page (index.html) with country picker | Must | M | Hero section shows country cards (flag + name + NRI count). Clicking a country navigates to `/us.html`, `/ca.html`, etc. |
| 1.5.3.4 | Mobile-responsive country switcher | Must | S | Country dropdown works on mobile. No horizontal scroll. Touch-friendly. |
| 1.5.3.5 | Auto-detect country from registration data | Could | S | If user has registered, default to their country. Override-able via dropdown. |

### Epic 1.5.4: Global vs Local Content Tagging

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 1.5.4.1 | Add `scope` field to summary schema | Must | S | Each summary has `"scope": "global"` or `"scope": "local"`. Scraper sets this based on source country profile. |
| 1.5.4.2 | Publisher merges global + local cards per country page | Must | S | Country page shows global cards (from India sources) + local cards (from that country's sources). Global cards have a subtle "Applies to all NRIs" indicator. |
| 1.5.4.3 | Deduplication across countries | Should | S | If same RBI circular appears in multiple country feeds, show it once per feed, not duplicated. Hash-based dedup. |

---

## Phase 2 — Gulf Expansion + Monetization v1

**Goal:** Add UAE and Saudi Arabia. Launch first monetization streams (affiliate + starter kits). Build Guides and Compare tabs.

**Target:** April 2026

### Epic 2.1: Gulf Country Profiles

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 2.1.1 | Create country profile: UAE | Must | L | `countries/ae.json` with MOHRE, ICA/ICP, FTA sources. Handle English + Arabic pages (prefer English mirrors). At least 5 active sources. |
| 2.1.2 | Create country profile: Saudi Arabia | Must | L | `countries/sa.json` with Qiwa, Absher, MISA, ZATCA sources. Handle Arabic-dominant pages. At least 4 active sources. |
| 2.1.3 | Add Arabic text handling to scraper | Must | M | Scraper detects Arabic content and passes it to summarizer with language hint. Summarizer outputs in English regardless. |
| 2.1.4 | Add Embassy/Consulate sources per country | Should | M | Indian Embassy/High Commission source for each country (e.g., `indembassyuae.gov.in`). Tagged as GLOBAL scope but country-specific consular notices. |

### Epic 2.2: Guides Tab

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 2.2.1 | Build Guides tab UI layout | Must | M | Third tab in navigation. Grid of guide cards. Each card: title, country flag, step count, "Start" CTA. Mobile-responsive. |
| 2.2.2 | Build guide template system | Must | M | Guide data stored as JSON (`guides/{code}-starter.json`). Publisher renders into static HTML guide pages. Each step has: description, source link, checkbox (localStorage). |
| 2.2.3 | Create guide: "Moving to UAE from India" | Must | L | 30-50 verified steps. Pre-departure + Week 1 + Month 1 + Ongoing sections. Every step has source link. |
| 2.2.4 | Create guide: "Moving to USA from India" | Must | L | 30-50 verified steps. Visa, SSN, banking, tax registration, FBAR setup. |
| 2.2.5 | Create guide: "Returning to India" (generic) | Must | L | Account conversion, tax re-entry, NRE→resident conversion, property considerations. |
| 2.2.6 | Create guide: "NRI Buying Property in India" | Should | M | FEMA rules, POA process, TDS requirements, repatriation rules. |
| 2.2.7 | Migrate existing Checklist into Guides tab | Should | S | Current Phase 1 checklist becomes a guide: "NRI Compliance Self-Audit". Same client-side-only privacy model. |
| 2.2.8 | Add compliance calendar per country | Could | M | Key annual deadlines rendered as a visual timeline within Guides. Data from country profile JSON. |

### Epic 2.3: Compare Tab

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 2.3.1 | Build Compare tab UI layout | Must | M | Tab shows comparison tables. User selects category + countries to compare. Clean table rendering on mobile (horizontal scroll or card view). |
| 2.3.2 | Create comparison data schema | Must | S | JSON schema for comparison tables: `compare/{category}.json`. Each entry: question, answers per country, source links per answer. |
| 2.3.3 | Create comparison: Banking & Accounts | Must | M | NRE/NRO rules, account types, FCNR, joint account rules — compared across 7 countries. |
| 2.3.4 | Create comparison: Tax Obligations | Must | M | Dual taxation, DTAA benefits, filing deadlines, worldwide income rules — compared across 7 countries. |
| 2.3.5 | Create comparison: Investments | Should | M | Mutual funds, direct equity, PPF eligibility, PFIC traps, PIS — compared across 7 countries. |
| 2.3.6 | Create comparison: Insurance | Should | M | Health insurance requirements, life insurance portability, travel insurance — compared across 7 countries. |
| 2.3.7 | Create comparison: Property | Could | M | Buying/selling property in India from abroad — FEMA + tax by country. |
| 2.3.8 | Create comparison: Remittance | Could | S | LRS limits, TCS rates, channels — information only, no product recommendations. |

### Epic 2.4: Monetization v1 — Affiliate Integration

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 2.4.1 | Design contextual partner card component | Must | S | HTML/CSS component: "Verified Partners" card. Clearly labelled. Visually distinct from editorial cards. Shows partner name, one-line description, CTA button. |
| 2.4.2 | Build affiliate link registry | Must | S | JSON file `monetization/partners.json` mapping partner → affiliate URL → category → target countries. Publisher injects contextual cards based on content category match. |
| 2.4.3 | Integrate remittance partners (Wise, Remitly) | Must | S | Affiliate cards appear below LRS/remittance-related content cards. Track clicks via UTM parameters. |
| 2.4.4 | Integrate tax filing partners (ClearTax NRI) | Must | S | Affiliate cards appear below ITR/FBAR deadline cards. |
| 2.4.5 | Add affiliate disclosure footer | Must | S | *"Some links on this page are affiliate links. We may earn a commission at no extra cost to you. This does not affect our editorial independence."* |
| 2.4.6 | Build Starter Kit landing pages | Should | M | Static pages for each kit ($29-49). Description, table of contents, purchase CTA. Payment via Gumroad/Lemon Squeezy (no custom payment system). |
| 2.4.7 | Create first Starter Kit: "UAE NRI Starter Kit" | Should | L | PDF + Google Sheet. 50-step checklist, compliance calendar, editable tracker. Priced at $39. |

---

## Phase 3 — Intelligence Engine + Pro Tier

**Goal:** Launch Search Discoverer and Trend Sensor engines. Build SmartNRI Pro subscription. Make Ask tab functional.

**Target:** May–June 2026

### Epic 3.1: Search Discoverer Engine

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 3.1.1 | Integrate Google Custom Search API | Must | M | New engine module: `pipeline/discoverer.py`. Queries configurable per country profile (`search_queries[]`). Returns candidate URLs. |
| 3.1.2 | Build LLM-based relevance classifier | Must | M | LLM classifies each search result: "actionable_regulatory" vs "news_noise" vs "ceremonial". Only actionable items proceed to summarizer. |
| 3.1.3 | Source verification step | Must | M | For each actionable candidate, attempt to find the official government source URL. If found → GREEN badge. If not → ORANGE or UNVERIFIED. |
| 3.1.4 | Integrate discoverer into main pipeline | Must | S | main.py runs: source_scraper → discoverer → merge → summarizer → publisher. Discoverer items clearly tagged as discovery-sourced. |
| 3.1.5 | Rate limiting and cost controls | Must | S | Max 20 search API calls per pipeline run. LLM classification uses cheapest model (gpt-4o-mini / gemini-flash). Daily cost cap configurable via .env. |

### Epic 3.2: Trend Sensor Engine

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 3.2.1 | Integrate Google Trends API | Should | M | New module: `pipeline/trend_sensor.py`. Monitors NRI-related queries by country. Outputs trending topics to `data/trends.json`. |
| 3.2.2 | Integrate Reddit API | Should | M | Monitor r/nri, r/IndiaInvestments, r/dubai, r/ABCDesis. Extract question topics (NOT content). Feed to discoverer. |
| 3.2.3 | Build topic-to-query translator | Should | S | LLM converts trending topic ("UAE job ban confusion") into search queries ("UAE labour ban period MOHRE 2026"). Feeds Engine 2. |
| 3.2.4 | Trend-based BLUE badge cards | Should | S | Cards originating from trend sensor get BLUE badge with note: "Trending topic — verified against official sources." |

### Epic 3.3: SmartNRI Pro Subscription

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 3.3.1 | Build WhatsApp Business API integration | Must | L | Daily digest sent via WhatsApp to Pro subscribers. Per-country digest. Uses WhatsApp Business Cloud API. |
| 3.3.2 | Build email digest (SendGrid) | Must | M | Weekly email digest as fallback. Uses SendGrid. Per-country segmentation based on registration data. |
| 3.3.3 | Set up payment (Stripe/Lemon Squeezy) | Must | M | $5/month subscription. Payment page. Webhook to add subscriber to WhatsApp list. |
| 3.3.4 | Build early RED alert system | Should | M | RED-badge items push immediately to Pro subscribers (WhatsApp + email). Not batched with daily digest. |
| 3.3.5 | Build quarterly compliance summary generator | Could | L | LLM generates a PDF summary of all regulatory changes in the past quarter, per country. Sent to Pro subscribers. |

### Epic 3.4: Ask Tab — Functional

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 3.4.1 | Build question submission form | Must | M | User submits question. Stored in `data/questions/pending.json`. No PII beyond registration data. |
| 3.4.2 | Build AI answer pipeline | Must | L | LLM receives question → searches for official answer → generates verified response with source links → outputs to `data/questions/answered.json`. |
| 3.4.3 | Publish answered questions as permanent cards | Must | M | Publisher renders answered questions as searchable, indexable pages. Builds SEO content library over time. |
| 3.4.4 | "Flag This Answer" button | Should | S | Users can flag inaccurate answers. Flagged items queued for re-verification. |
| 3.4.5 | Pro tier: Priority answer queue | Should | S | Pro subscribers' questions processed within 24 hours. Free tier: best-effort within 7 days. |
| 3.4.6 | Build FAQ library from answered questions | Should | M | Top 50 most-asked questions curated into a permanent FAQ page per country. |

---

## Phase 4 — Scale + B2B + Top 20 Expansion

**Goal:** Expand to remaining top 20 countries. Launch B2B monetization. Enterprise API.

**Target:** Q3-Q4 2026

### Epic 4.1: Country Expansion

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 4.1.1 | Create country profile: Kuwait | Must | M | Sources: PAM, MOI. Limited digital presence — rely more on discoverer engine. |
| 4.1.2 | Create country profile: Qatar | Should | M | Sources: MOI, MADLSA. |
| 4.1.3 | Create country profile: Oman | Should | M | Sources: ROP, MOHE. |
| 4.1.4 | Create country profile: UK | Should | M | Sources: HMRC, Home Office. |
| 4.1.5 | Create country profile: Australia | Should | M | Sources: ATO, DHA. |
| 4.1.6 | Create country profile: Bahrain | Could | M | Sources: LMRA, MOI. |
| 4.1.7 | Create country profile: Germany | Could | M | Sources: BAMF, Finanzamt. |
| 4.1.8 | Remaining top 20 countries | Could | XL | Nepal, Italy, NZ, Philippines. Add as country profiles. |

### Epic 4.2: Sponsored Verified Cards (B2B)

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 4.2.1 | Build sponsored card submission portal | Must | L | Simple form: partner submits content + source URLs. AI verifies claims against official sources. If passes → published with "Sponsored · Verified" badge. |
| 4.2.2 | Build billing for sponsored cards | Must | M | $500-2,000/month per card. Stripe subscription. Auto-expire after billing period. |
| 4.2.3 | Build sponsored card performance dashboard | Should | M | Partner sees: impressions, clicks, CTR. Simple static report, not a real-time dashboard. |

### Epic 4.3: Enterprise API

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 4.3.1 | Build REST API for verified NRI data | Must | XL | FastAPI service. Endpoints: `/api/v1/updates/{country}`, `/api/v1/compare/{category}`, `/api/v1/guides/{slug}`. API key auth. |
| 4.3.2 | Rate limiting and API key management | Must | M | Tiered plans: Free (100 calls/day), Pro ($99/month, 5K calls/day), Enterprise (custom). |
| 4.3.3 | API documentation | Must | M | OpenAPI/Swagger docs. Quick-start guide. Example integrations. |

### Epic 4.4: Distribution Channels

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| 4.4.1 | Launch WhatsApp Channel per country | Must | M | Public WhatsApp Channels (not groups). Weekly digest pushed automatically. |
| 4.4.2 | Telegram Channel per country | Should | S | Mirror of WhatsApp content. Already have Telegram bot infrastructure. |
| 4.4.3 | SEO optimization for transition guides | Should | M | Meta tags, structured data, sitemap. Target: "moving to UAE from India checklist" etc. |
| 4.4.4 | Embed widget for partner sites | Could | L | Lightweight JS widget that banks/fintechs can embed to show SmartNRI verified updates. |

---

## Backlog — Ideas (Unprioritised)

These ideas are captured but not yet scheduled. They may be promoted to a phase during planning.

| ID | Idea | Category | Notes |
|---|---|---|---|
| BL-01 | "SmartNRI Score" — compliance health score per user | Feature | Gamification. Based on checklist completion. "Share My Score" viral mechanic. |
| BL-02 | "Trust Score" on every card — "Verified against 3 sources, last checked 2h ago" | Feature | Brand differentiator. Shows real-time verification freshness. |
| BL-03 | Push notifications (PWA) | Feature | Progressive Web App with push for RED alerts. Alternative to WhatsApp Pro. |
| BL-04 | Dark mode | Feature | User preference toggle. CSS-only implementation. |
| BL-05 | Multi-language UI (Hindi, Tamil, Malayalam, Arabic) | Feature | High impact for Gulf NRIs. Significant effort. Phase 4+. |
| BL-06 | NRI community map — "How many NRIs near me?" | Feature | Privacy-safe aggregate counts by city. Visualization layer. |
| BL-07 | Podcast / audio digest | Content | Weekly 10-min audio summary. AI-generated voice. Distribute via Spotify/Apple. |
| BL-08 | "NRI Myth Buster" series | Content | Debunk viral WhatsApp forwards with verified sources. High shareability. |
| BL-09 | Offline mode (PWA cache) | Feature | Cache last 7 days of content. Critical for users with intermittent connectivity. |
| BL-10 | Integration with SBNRI/Vance APIs | Partnership | Embed their tools within Compare tab. Revenue share model. |
| BL-11 | "Country vs Country" tool | Feature | "I'm considering moving from UAE to Canada — compare my NRI obligations side by side." |
| BL-12 | Annual "State of NRI" report | Content | Data-driven report on regulatory changes, trends, demographics. PR + lead gen asset. |

---

## UX Psychology — "Premium Clarity" (Accepted Items)

Based on "Premium Website Psychology" review. Only the 30% that applies to a compliance/reference platform. Design philosophy: **"Clarity for Complexity"** (Stripe model, not Apple/Hermes luxury model).

### Epic UX.1: 50-Millisecond Trust Test (Phase 1)

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| UX.1.1 | Redesign hero section for authority signals | Must | M | First viewport communicates: "Verified against [N] government sources across [N] countries." No generic stock images. Badge count + source count + country count visible instantly. Clean, data-focused layout with high-contrast typography. |
| UX.1.2 | Add trust indicators above the fold | Must | S | Show: total verified sources, countries covered, last pipeline run timestamp. User sees credibility proof in < 1 second. Professional not playful — think GOV.UK, not Apple. |
| UX.1.3 | Remove decorative elements that don't build trust | Should | S | Audit current UI: remove animations, gradients, or visual elements that say "pretty" but don't say "trustworthy." Replace CSS globe art with something that communicates authority (e.g., clean country flags, verification badge count). |

### Epic UX.2: Cognitive Fluency — Scanability (Phase 1.5)

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| UX.2.1 | Optimize card layout for 3-second scanning | Must | M | On mobile, a single card is scannable without scrolling: badge colour visible (distinguishable without reading text), "So What?" line readable in one glance, source link tappable in one tap. Test: can a user identify "what changed and should I care?" in 3 seconds? |
| UX.2.2 | Implement visual hierarchy for badge priority | Must | S | RED cards visually dominate (urgent). GREEN cards are calm (informational). Card ordering: RED > GREEN > ORANGE > BLUE. Badge icons supplement colours for colour-blind accessibility. |
| UX.2.3 | Simplify country switcher for instant use | Should | S | Country selector requires exactly 1 tap/click. No dropdowns within dropdowns. Country flags as visual anchors. Current country always visible. Works flawlessly on mobile with fat-finger tolerance. |
| UX.2.4 | Reduce cognitive load on Compare tables | Should | M | Comparison tables on mobile: card-based layout (not wide tables requiring horizontal scroll). Each row becomes a question-card with country answers stacked vertically. User answers their question without parsing a grid. |

### Epic UX.3: Clean End-States — Peak-End Rule (Phase 2)

| ID | Story | Priority | Size | Acceptance Criteria |
|---|---|---|---|---|
| UX.3.1 | Add "Download as PDF" to all guides | Must | S | Every guide and comparison table has a prominent "Download as PDF" button. NRIs use this at government offices, embassy appointments, and bank visits. Print-friendly formatting. |
| UX.3.2 | Add "Share on WhatsApp" to all content | Must | S | Every card, guide, and comparison table has a 1-tap "Share on WhatsApp" button. Pre-formats a clean message with title + link. This is the primary distribution mechanism. |
| UX.3.3 | Design clean guide completion state | Should | S | When a user completes a checklist/guide (all items checked), show a clean summary: "X of Y steps complete. Download your checklist. Share with a friend." No celebratory animations — just clear, professional next actions. |
| UX.3.4 | Add source verification display on every card | Must | S | Every card shows: source link (clickable), source quote (exact text from document), "Last Verified" timestamp. This IS the trust architecture made visible. Users can verify any card in 10 seconds. |

---

## Technical Debt & Infrastructure

| ID | Item | Priority | Size | Notes |
|---|---|---|---|---|
| TD-01 | Add requirements.txt with pinned versions | Must | S | Security: prevent dependency attacks. Currently no requirements.txt. |
| TD-02 | Add pytest test suite for pipeline | Must | M | At minimum: test scraper output schema, test summarizer JSON parsing, test publisher HTML injection. |
| TD-03 | Set up GitHub Actions CI | Must | M | Run tests on PR. Lint Python. Secret scan. |
| TD-04 | Set up GitHub Actions daily pipeline cron | Must | M | `.github/workflows/daily_update.yml` — trigger pipeline, commit updated HTML, deploy. |
| TD-05 | Dockerize pipeline (not just frontend) | Should | M | Pipeline runs inside Docker container. Consistent environment across dev and VPS. |
| TD-06 | Add structured logging (JSON format) | Should | S | Machine-parseable logs for monitoring. |
| TD-07 | Add content hash verification on published cards | Should | S | Detect if published card's source URL has changed since publication. |
| TD-08 | Rate limiting for scraper across all countries | Must | S | Configurable delay between requests. Per-domain rate limits. Don't get IP-banned. |
| TD-09 | Add retry logic for LLM API failures | Should | S | Exponential backoff. Fallback from primary to secondary LLM provider. |
| TD-10 | SEO: Generate sitemap.xml dynamically | Should | S | Publisher generates sitemap.xml listing all country pages and guide pages. |

---

## Sprint Planning Guide

Each sprint = 2 weeks. Recommended sprint structure:

**Sprint 0 (Week 0):** Hero guide ("Return to India") + 3 affiliate signups + UX.1 (Trust Test hero redesign)
**Sprint 1 (Week 1-2):** Epic 1.5.1 (Country profiles) + TD-01 + TD-02 + UX.1.2 (Trust indicators)
**Sprint 2 (Week 3-4):** Epic 1.5.2 (Pipeline refactor) + Epic 1.5.4 (Global/local tagging) + UX.2.1-2.2 (Card scanability)
**Sprint 3 (Week 5-6):** Epic 1.5.3 (Frontend country switcher) + TD-03 + TD-04 + UX.2.3 (Country switcher UX) + UX.3.4 (Source quote display)
**Sprint 4 (Week 7-8):** Epic 2.1 (Gulf profiles) + Epic 2.2.1-2.2.2 (Guides tab foundation) + UX.3.1-3.2 (PDF download + WhatsApp share)
**Sprint 5 (Week 9-10):** Epic 2.3 (Compare tab) + Epic 2.4.1-2.4.5 (Affiliate integration) + UX.2.4 (Compare table mobile UX)
**Sprint 6 (Week 11-12):** Epic 2.2.3-2.2.6 (Guide content creation) + Epic 2.4.6-2.4.7 (Starter kits) + UX.3.3 (Guide completion state)
