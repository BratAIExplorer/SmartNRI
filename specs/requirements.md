# SmartNRI — Product Requirements

**Version:** 2.1 | **Phase:** 1.5 → 4 (Global NRI) | **Date:** 23 Feb 2026
**Audit Inputs:** GPT Strategic Audit + Gemini Autonomous Framework — reviewed and incorporated 23 Feb 2026

---

## Problem Statement

Indian expats (NRIs) across 20+ countries have no single, trustworthy, non-commercial reference for navigating the intersection of host-country regulations and Indian government rules. Existing platforms (SBNRI, Vance, INDmoney) are transactional — they sell financial products. WhatsApp groups and Reddit threads spread unverified claims. The result: confusion, missed deadlines, compliance risk, and financial penalties.

The problem scales with geography. An NRI in UAE faces labour law + visa + FEMA + tax issues simultaneously. An NRI in USA faces IRS worldwide taxation + FBAR + PFIC traps + FEMA. Each country has unique pain points, but ~40% of the regulatory burden (India-side rules) is identical for ALL NRIs worldwide.

---

## Vision

> *"Every Indian abroad deserves one place to find the truth — verified, current, and free."*

## Mission

> *"SmartNRI maps the regulatory landscape for Non-Resident Indians across 7+ countries, connecting 18 million NRIs to government-verified intelligence on tax, immigration, banking, and compliance — autonomously, without selling financial products, and without requiring a single human editor."*

## Tagline

> *"The truth before the transaction."*

## Core Identity

- **What we are:** The Map — a navigator that finds, verifies, and links NRIs to official government sources. We curate, we don't advise.
- **What we are NOT:** A financial advisor, a services marketplace, a bank, or a source of original legal opinion.
- **Business model:** B2C-first (individual NRIs), B2B-as-a-byproduct (advisors/fintechs find us through traffic).
- **Ambition:** Lifestyle business operations (hands-free, solo founder), positioned as acquisition target by Year 2-3.
- **Language rule:** Never say "you should" or "we recommend." Say "the RBI circular states" and "the MOHRE portal confirms."

---

## Strategic Positioning

| Segment | Competitors | SmartNRI Differentiator |
|---|---|---|
| Fintech / Remittance | SBNRI, Wise, Remitly | Product-agnostic truth BEFORE the transaction |
| Investment | Sarwa, INDmoney, Groww NRI | Regulatory compliance education, not trading |
| Gov / Utility | Absher, ICA, Passport Seva | Aggregates and translates gov-speak into actionable NRI intelligence |
| Manual / Social | Reddit, FB Groups, WhatsApp | Verified facts vs. anecdotal rumours |

**Market Gap:** Most NRI apps are "banks in disguise." SmartNRI is a Pure-Play Intelligence Platform that doesn't require a bank account to be useful.

---

## Target Audience

### Primary Markets (Phase 1.5 — 2)

| Rank | Country | NRI Population | Launch Priority | Reason |
|---|---|---|---|---|
| 1 | UAE | 3.89M | Phase 2 | Largest NRI hub, English gov portals exist |
| 2 | Saudi Arabia | 2.75M | Phase 2 | Second largest, some Arabic-only portals |
| 3 | USA | 2.07M | Phase 1.5 | English, excellent gov portal quality |
| 4 | Canada | 1.75M | Phase 1.5 | English, excellent gov portals, RSS feeds |
| 5 | Kuwait | 1.01M | Phase 3 | Poor digital presence, lower priority |
| 11 | Singapore | 350K | Phase 1.5 | English, excellent portals (MOM, IRAS) |
| 14 | Malaysia | 185K | Phase 1 (Done) | Foundation market, already built |

### Secondary Markets (Phase 4+)
Qatar, Oman, UK, Australia, Bahrain, Germany, Italy, New Zealand, Philippines, Nepal

### Entry Channel
WhatsApp sharing among trusted NRI networks + SEO via transition guides

---

## The Two-Layer Content Model

All content falls into exactly two categories:

| Layer | Scope | Example | Publishing |
|---|---|---|---|
| **GLOBAL** (India-side) | Affects ALL NRIs regardless of country | RBI circular on NRE/NRO, Budget TCS changes, OCI rule updates, FEMA compliance | Write once, serve on every country feed |
| **LOCAL** (Host-country) | Affects NRIs in THAT country only | UAE golden visa change, US FBAR deadline, Canada PR tax implications | Country-specific feed only |

**Key insight:** ~40% of content is GLOBAL. This means adding a new country does NOT require 2x the content — only the LOCAL layer is new.

---

## Core Features

### Tab 1: Signal (Daily Verified Updates)

**Purpose:** Auto-generated daily digest of government regulatory updates relevant to NRIs.

**Content per card:**
- Verification badge (GREEN / ORANGE / BLUE / RED / UNVERIFIED)
- Short punchy headline (max 12 words)
- One-line "So What?" summary (max 25 words)
- 1–3 actionable bullet points (each starting with a verb)
- Direct clickable link to the official source document
- Source name and publication date
- Footer disclaimer: *"This is a reference guide. Verify with the linked official source before taking action."*

**Country filtering:**
- User selects their country of residence (persisted in localStorage)
- Feed shows: ALL global cards + LOCAL cards for selected country
- Country switcher at top of feed (dropdown or tabs for top 7 countries)
- URL structure: `smartnri.com/uae`, `smartnri.com/usa`, etc.

**Auto-refresh:** Pipeline runs every 24 hours. 3–5 new items per run.

**Badge system:**

| Badge | Label | Criteria | Colour |
|---|---|---|---|
| GREEN | Official | Direct link to `.gov.in`, `.gov.my`, `.gov.ae`, `.gov.sa`, `.gov`, `.gc.ca` | Green |
| ORANGE | Expert | Reputable news or professional advisory (KPMG, Big4, ET, law firm) | Orange |
| BLUE | Community | Trending topic verified against Tier 1 by the AI | Blue |
| RED | Alert | Urgent, time-sensitive action required (deadline < 30 days) | Red |
| UNVERIFIED | Flagged | No government source found — display with strong disclaimer | Grey |

### Tab 2: Guides (Transition Checklists + Compliance Calendars)

**Purpose:** Evergreen, high-value reference content for NRIs at key life transitions.

**Transition Checklists (per country):**
- "Moving from India to [Country]" — pre-departure + first 90 days
- "Returning to India after [Country]" — tax re-entry + account conversion
- "NRI Buying Property in India from [Country]" — FEMA + tax + POA
- "NRI Marriage / Child Born Abroad" — documentation checklist
- Each checklist: 15–30 verified steps with source links
- Interactive: checkbox state saved in localStorage (client-side only)

**Compliance Calendar (per country):**
- Key annual deadlines: ITR filing, FBAR (USA), tax residency determination date
- Visual timeline / month-by-month view
- Countdown badges for upcoming deadlines (30/60/90 day warnings)

**Self-Audit Checklist (from Phase 1, enhanced):**
- Banking Compliance: NRE/NRO status, FEMA declaration, nominee registration
- Document Reminders: Type (dropdown) + expiry date only. No document uploads. No PII.
- Investment Audit: PIS account, FATCA, prohibited investments (PPF for NRIs, agricultural land)
- "No Change" shortcut on 6-month re-check

**Privacy:** *"We never store account numbers, document scans, or personal financial data. This checklist runs entirely in your browser."*

### Tab 3: Compare (Regulatory Comparison Tables)

**Purpose:** Side-by-side comparison of rules across countries. The "investment and insurance" need addressed through education, not product recommendations.

**Comparison tables (examples):**

| Question | India (NRI) | UAE | USA | Canada | Singapore |
|---|---|---|---|---|---|
| Can I hold mutual funds? | Yes (PIS) | Yes (local) | Yes (PFIC trap) | Yes (local) | Yes (local) |
| NRE FD interest taxable? | No (India) | No (no tax) | Yes (IRS) | Yes (CRA) | No |
| Can I buy property in India? | Yes (FEMA rules) | N/A | Yes (FEMA) | Yes (FEMA) | Yes (FEMA) |
| Health insurance options? | NRI plans | Mandatory employer | ACA/employer | Provincial + private | MediShield |

**Categories:**
- Banking & Accounts (NRE/NRO/FCNR rules by country)
- Tax Obligations (dual taxation, DTAA benefits by country)
- Investments (what's allowed, what's trapped, what's prohibited)
- Insurance (health, life, travel — regulatory requirements by country)
- Property (buying/selling in India from abroad — FEMA + tax)
- Remittance (LRS limits, TCS, best channels — information only)

**Monetization hook:** Below each comparison table:
> *"Need help acting on this? These verified partners can assist:"*
> [Contextual affiliate links — clearly separated from editorial content]

### Tab 4: Ask (User Questions + Verified Answers)

**Purpose:** User-submitted questions → AI-verified answers with source links.

**Phase 1.5 (current):**
- Search bar with "Coming Soon" placeholder
- Pre-populated suggested questions (8 chips)
- Trusted Voices section: Curated grid of recommended YouTube/Instagram channels (links only, no content reproduction)

**Phase 3 (future):**
- User submits question
- AI searches for the official government answer
- Verified answer published as a permanent card (builds SEO content library)
- Pro tier: Priority answer queue
- "Flag This Answer" button for community corrections
- Every answered question becomes permanent, searchable content

---

## Registration Gate

- **Trigger:** First page load + clicking Guides/Compare/Ask tabs
- **Fields (all required):**
  - First Name
  - Email Address
  - Country of Residence (dropdown: UAE, Saudi Arabia, USA, Canada, Kuwait, Singapore, Malaysia, UK, Australia, Germany, Qatar, Oman, Other)
  - Role: Salaried Employee / Business Owner / Freelancer / Student / Retired / Other
- **Storage:** `localStorage` key `snri_user` (JSON) — no server-side call yet
- **Gate behaviour:**
  - Signal tab freely visible (content teaser for shareability)
  - Guides, Compare, and Ask tabs gated until registered
  - Registration persists across sessions
- **Backend hook:** `fetch('/api/register', ...)` ready to wire
- **Purpose:** Build email list, understand country distribution, segment for WhatsApp digest

---

## Country Profile System

Each supported country is defined as a JSON profile. Adding a new country = adding a JSON file.

**Profile schema:**
```json
{
  "country_code": "AE",
  "display_name": "UAE",
  "flag_emoji": "🇦🇪",
  "timezone": "Asia/Dubai",
  "languages": ["en", "ar"],
  "currency": "AED",
  "topics": ["visa", "labour_law", "tax", "banking", "driving", "property"],
  "sources": [
    {
      "id": "mohre",
      "name": "Ministry of Human Resources (MOHRE)",
      "url": "https://www.mohre.gov.ae/en/...",
      "scrape_method": "html",
      "tier": 1,
      "badge": "GREEN",
      "selectors": { "title": "h3.news-title", "body": "div.news-body" }
    }
  ],
  "search_queries": [
    "UAE visa rules Indian workers 2026",
    "golden visa India eligibility"
  ],
  "compliance_calendar": [
    { "month": 3, "day": 31, "event": "UAE tax return deadline (if applicable)", "source": "..." }
  ]
}
```

**Source registry per country:**

**UAE:**
- MOHRE (mohre.gov.ae) — Labour law, work permits, job changes
- ICA/ICP (icp.gov.ae) — Visa categories, golden visa, residence permits
- Federal Tax Authority (tax.gov.ae) — Corporate tax, VAT for businesses
- Dubai Economy (dubaided.gov.ae) — Business licensing

**Saudi Arabia:**
- Qiwa (qiwa.sa) — Labour law, work permits, contract management
- Absher (absher.sa) — Visa, iqama, exit/re-entry permits
- Ministry of Investment (misa.gov.sa) — Business setup, investment rules
- ZATCA (zatca.gov.sa) — Tax and customs

**USA:**
- IRS (irs.gov) — Tax filing, FBAR, FATCA, worldwide income rules
- USCIS (uscis.gov) — Visa categories, green card, citizenship
- State Department (state.gov) — Passport, OCI interactions
- SSA (ssa.gov) — Social Security for NRIs

**Canada:**
- CRA (canada.ca/cra) — Tax residency, NRI filing obligations
- IRCC (canada.ca/ircc) — Immigration, PR, work permits
- FINTRAC — Financial reporting obligations

**Singapore:**
- MOM (mom.gov.sg) — Employment Pass, work permits
- IRAS (iras.gov.sg) — Tax residency, filing obligations
- MAS (mas.gov.sg) — Banking, investment regulations

**Malaysia (existing):**
- ESD/IMI, HASIL, JPJ, BNM, MDEC (already in sources.json)

**India (GLOBAL — serves all countries):**
- Income Tax India (incometaxindia.gov.in)
- RBI (rbi.org.in) — NRE/NRO/FEMA master circulars
- MEA (mea.gov.in) — OCI, passport policies
- SEBI (sebi.gov.in) — PIS, investment limits
- HCI/Embassy sites per country

---

## Three-Engine Discovery Architecture

### Engine 1: Source Scraper (existing, generalized)
- Reads country profile → fetches from listed gov sources
- Deduplicates via content hashing
- Works for structured sites with stable HTML

### Engine 2: Search Discoverer (new)
- Uses Google Custom Search API / News API to find regulatory news
- Query patterns: `"{country} India visa tax law change 2026"`
- LLM classifies results: actionable vs. noise vs. ceremonial
- Finds and verifies against official source links
- Feeds candidates to the summarizer

### Engine 3: Trend Sensor (new)
- Google Trends API — NRI-related query monitoring by country
- Reddit API — r/nri, r/IndiaInvestments, r/dubai, r/ABCDesis
- YouTube Data API v3 — trending search queries (NOT video content)
- Detects what NRIs are searching for RIGHT NOW
- Feeds topics back to Engine 2 for verification

**Pipeline flow:**
```
Trend Sensor → what are NRIs asking?
     ↓ topics
Search Discoverer → find regulatory news
     ↓ candidates
Source Scraper → verify against gov sites
     ↓ verified items
Summarizer → LLM: "So What?" + badge
     ↓
Publisher → per-country HTML / feed
```

---

## Monetization Strategy

### Principles
1. **Never gate content.** All information stays free on the website
2. **Never recommend products.** Compare rules. Let affiliate links sit below education
3. **Trust test:** Every monetization decision must pass: *"Does this make users trust us MORE or LESS?"*
4. **Sell convenience, not access.** Charge for speed, format, and delivery

### Revenue Stream 1: Contextual Affiliate Partners

Curated, small list of verified partners per category. Not a marketplace.

| Category | Example Partners | Revenue Model | Trigger |
|---|---|---|---|
| Remittance | Wise, Remitly, InstaReM | $5-15 per signup | Card about LRS/remittance rules |
| NRI Tax Filing | ClearTax NRI, SBNRI Tax, local CPAs | $30-80 per lead | Card about ITR/FBAR deadlines |
| Health for Parents | MediBuddy, Apollo 24/7, Max@Home | $10-25 per subscription | Guide about parent care |
| Legal / POA | NRI Legal Services, LegalDesk | $20-50 per consultation | Guide about property/POA |
| Insurance | Digit, HDFC Ergo (travel/health) | $15-40 per policy | Compare tab insurance section |
| Property Management | NoBroker NRI, HouseJoy | $20-50 per signup | Guide about property from abroad |

**Placement:** Contextual partner cards appear WITHIN relevant content, clearly labelled as "Verified Partners", separated from editorial content. Never inside the card itself.

### Revenue Stream 2: Country Starter Kits ($29-49)

Paid digital products for NRIs at transition points.

| Kit | Price | Contents |
|---|---|---|
| UAE Starter Kit | $39 | 50-step checklist, compliance calendar, editable tracker sheet |
| USA Tax Kit | $49 | FBAR + FATCA guide, ITR cross-filing, DTAA optimization |
| Canada PR Kit | $39 | Tax residency transition, CRA filing, NRE/NRO conversion |
| Return to India Kit | $29 | Account conversion, tax re-entry, property transfer |

Zero marginal cost. Solves high-stress, one-time problems. Builds email list.

### Revenue Stream 3: SmartNRI Pro ($5/month)

| Feature | Free | Pro |
|---|---|---|
| Weekly updates on website | Yes | Yes |
| Daily WhatsApp/email digest | No | Yes |
| Early RED alerts (visa/tax deadlines) | No | Yes |
| Quarterly compliance summary PDF | No | Yes |
| Priority "Ask" queue | No | Yes |

### Revenue Stream 4: Sponsored Verified Cards (B2B — Phase 4+)

Banks, fintechs, and law firms pay to publish content as a verified card. Content must pass the same AI verification standard. Appears with "Sponsored · Verified" badge. $500-2,000/month per card.

**Revenue targets:**

| Phase | Streams | Monthly Target |
|---|---|---|
| Phase 1.5-2 | Affiliate + Starter Kits | $500–2,000 |
| Phase 2-3 | + SmartNRI Pro | $5,000–10,000 |
| Phase 3-4 | + Sponsored Cards | $15,000–30,000 |
| Phase 4+ | + Enterprise API | $50,000+ |

### What We Will NOT Build

| Trap | Why It Fails |
|---|---|
| Full services marketplace | Becomes customer support team. Bad vendor = brand damage |
| Investment advisory | SEBI/SEC/MAS licensing required per jurisdiction |
| Subscription wall on content | Kills SEO, kills WhatsApp shareability, kills growth |
| Banner ads / AdSense | Destroys credibility. $0.50 CPM isn't worth it |
| Our own fintech | We're intelligence, not banking. Partner, don't build |

---

## Quality & Trust Architecture (From External Audits)

These requirements were identified during GPT and Gemini strategic audits (23 Feb 2026) and accepted by the founder.

### "Source Match" Validation Architecture — Non-Negotiable

The founder is not a regulatory expert and cannot be expected to validate tax/visa accuracy manually. The system must validate ITSELF, making accuracy verifiable by anyone without domain expertise.

**Every published card must include a Source Quote** — an exact excerpt from the government source that proves the summary. This makes validation trivially checkable by the founder, an intern, or end users.

**Automated Validation Flow:**
1. **Executor:** Summarizer generates summary + extracts a supporting quote from the raw source text
2. **Verifier (automated):**
   - Source URL returns HTTP 200? If 404 → SKIP, do not publish
   - Supporting quote exists verbatim in raw source text? (string match) If not → QUARANTINE
   - Summary contains no claims absent from raw text? (LLM check) If hallucination detected → QUARANTINE
3. **Critic (Phase 2+):** Second LLM pass reviews summary for factual drift against source text

**Publishing rules:**
- All 3 automated checks pass + badge is GREEN/ORANGE/BLUE → **AUTO-PUBLISH**
- Any automated check fails → **QUARANTINE** (founder reviews when available, no time pressure)
- Badge is RED (urgent/time-sensitive) → **ALWAYS QUARANTINE** regardless of checks
  - Telegram bot sends card + source quote + source link to founder
  - Founder replies "OK" (approve) or "NO" (reject) from phone (~30 seconds)
  - If no founder response within 48 hours → auto-publish with extra disclaimer: *"This alert has not been manually reviewed. Verify urgently with the linked source."*
  - Pipeline NEVER stalls. Worst case = weaker disclaimer, not silence

**Card display format (trust-building):**
```
[Badge] [Title]
[So What? summary]
[Bullet points]

Source: [clickable government link]
Source Quote: "[exact quote from document proving the summary]"
Last Verified: [date + time the URL was checked]
```

**If an intern is hired (Phase 2+), their checklist requires NO domain expertise:**
1. Click source link. Does it load? (Yes/No)
2. Find the source quote on the page. Is it there? (Yes/No)
3. Do the bullets say anything NOT in the source? (Yes/No)

**Founder effort by phase:**

| Phase | Method | Founder Time |
|---|---|---|
| Phase 1.5-2 | Source Match auto-validation + Telegram for RED items | ~15 min/week |
| Phase 2-3 | Same + optional intern spot-checks | ~5 min/week |
| Phase 3+ | + Critic LLM pass. Auto-publish non-RED. RED via Telegram | ~5 min/week |

### Adversarial Testing (Phase 2+)

- Feed the summarizer deliberately misleading inputs (fake circulars, ambiguous legal text) during testing
- Verify the system correctly flags or skips suspicious content
- Build into pytest test suite: `pipeline/tests/test_adversarial.py`

### Content Velocity Strategy

- **Phase 1.5-2:** Quality over velocity. 1 deeply researched guide per week > 5 shallow daily items
- **Phase 3+:** As trust is established, increase to 3-5 items daily via discovery engine
- Every published item must have a "freshness date" — when it was last verified against the source

### Gulf vs Western Content Segmentation

Gulf NRIs and Western NRIs have fundamentally different regulatory concerns:

| Concern Area | Gulf NRIs (UAE, Saudi, Kuwait) | Western NRIs (USA, Canada, Singapore) |
|---|---|---|
| Primary worry | Labour law, iqama/visa, job-loss consequences, exit permits | Tax (FATCA, FBAR), estate planning, retirement accounts |
| Gov interaction | Absher, Qiwa, MOHRE portals | IRS, CRA online filing, USCIS |
| Banking focus | Salary accounts, WPS, gold savings | 401k, RRSP, worldwide income reporting |
| Property | Less relevant (Gulf ownership restrictions) | FEMA compliance for India property from abroad |
| Language | Arabic + English | English |

Content, guides, and compare tables MUST reflect these differences. Generic "NRI" content doesn't resonate.

---

## Legal & Liability Requirements (From Gemini Audit)

### Disclaimers (Required on Every Page)

1. **General disclaimer:** *"SmartNRI is an independent reference guide. Verify with linked official sources before taking action."*
2. **No-advice disclaimer:** *"This platform provides general summary information and does not constitute legal, tax, or financial advice. Consult a qualified professional before making decisions."*
3. **Affiliate disclosure:** *"Some links on this page are from verified partners. We may earn a commission at no extra cost to you. This does not affect our editorial independence."*
4. **AI disclosure:** *"Content summaries are AI-generated from official government sources. While we verify accuracy, errors may occur. Always check the linked source."*

### Insurance Awareness (Phase 3+)

When SmartNRI has real users and revenue, the founder should secure:
- **Tech E&O insurance** — covers errors in AI-generated professional content
- **D&O insurance** — protects founder's personal assets
- **Cyber liability** — protects against data breaches
- Note: CGL policies in 2026 increasingly exclude AI-related claims (CG 40 47 endorsement). Seek affirmative AI coverage.

### Jurisdictional Clarity

- Platform operating jurisdiction must be clearly stated in Terms of Service
- Multi-jurisdictional notice required because NRIs operate across countries
- User certification workflow for high-risk outputs (e.g., tax calculators) — user acknowledges AI limitations before accessing

---

## Government API Preferences (From Gemini Audit)

Where available, prefer structured government APIs over HTML scraping:

| Country | API Source | Data Type | Advantage |
|---|---|---|---|
| USA | api.data.gov | Tax (Treasury), Commerce | Structured, stable, no HTML breakage |
| UAE | api.government.ae | Legislations, Payments | Official API marketplace |
| Saudi Arabia | dga.gov.sa (RAQMI) | Digital platforms, documents | Government-endorsed |
| India | RSS feeds (RBI, Income Tax) | Press releases, circulars | Structured, reliable |

APIs are more reliable than scraping, don't break when sites redesign, and are explicitly permitted by the government. Migrate from HTML scraping to APIs wherever possible during Phase 2-3.

---

## Distribution Strategy

### WhatsApp-First (Critical for Gulf Markets)

- WhatsApp IS the internet for Gulf NRIs. 85% open rates vs 20% for email
- Website = content engine. WhatsApp = distribution engine
- Phase 2: WhatsApp Channel per country (broadcast, unlimited followers, no interaction overhead)
- Phase 3: SmartNRI Pro delivers daily digest via WhatsApp Business API

### SEO as Long-Term Moat

- Evergreen guides target high-search queries: "moving to UAE from India checklist," "FBAR deadline NRI 2026," "returning to India after USA"
- Every answered question in Ask tab becomes a permanent, indexable page
- Sitemap.xml generated dynamically by publisher
- Structured data (JSON-LD) on all guide and comparison pages

### Cold Start Plan

1. Founder's personal NRI network (family, friends, colleagues across countries)
2. ONE viral guide shared in NRI WhatsApp groups ("Returning to India from UAE — Complete Checklist")
3. Reddit posts in r/nri, r/IndiaInvestments (share guide, not spam)
4. Measure engagement before scaling content production

### Offline Utility

- "Download as PDF" button on every guide and comparison table
- NRIs dealing with embassy appointments and government offices need printed references
- Trivially implementable, massively useful

---

## Privacy & Compliance Requirements

- Page load: < 2 seconds on 4G connection (any target country)
- Total page weight: < 60KB (Oat UI ~8KB + CSS ~5KB + content + country data)
- Fully readable with JavaScript disabled (content cards render as static HTML)
- Country switching: instant (no page reload — preloaded data or separate static pages)

---

## Accessibility & Compliance

- All interactive elements have unique IDs
- Alt text on all images
- Disclaimer footer pinned to bottom of every tab
- No advice language — informational only
- Colour-blind safe badge system (uses labels + icons, not colour alone)
- WCAG 2.1 AA target for all pages

---

## Definition of Done (by Phase)

### Phase 1.5 — Multi-Country Foundation
- [ ] Country profile schema defined and implemented
- [ ] USA, Canada, Singapore sources added and scraping
- [ ] Pipeline produces per-country output files
- [ ] Frontend country switcher working (dropdown + URL routing)
- [ ] Global vs local content separation working
- [ ] Pipeline runs end-to-end for 3+ countries

### Phase 2 — Gulf Expansion + Monetization v1
- [ ] UAE and Saudi Arabia sources added and scraping
- [ ] Contextual affiliate links integrated (remittance + tax filing)
- [ ] First Starter Kit published and purchasable
- [ ] Guides tab live with 2+ transition checklists
- [ ] Compare tab live with 3+ comparison tables

### Phase 3 — Intelligence Engine + Pro Tier
- [ ] Search Discoverer engine operational
- [ ] Trend Sensor feeding topics to pipeline
- [ ] SmartNRI Pro subscriptions live (WhatsApp digest)
- [ ] Ask tab functional (user questions → verified answers)
- [ ] 50+ answered questions in content library

### Phase 4 — Scale + B2B
- [ ] Kuwait + remaining top 20 countries added
- [ ] Sponsored Verified Cards program live
- [ ] Enterprise API for partner integration
- [ ] 100K+ monthly visitors
- [ ] Self-sustaining revenue ($15K+/month)
