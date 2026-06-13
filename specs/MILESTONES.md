# SmartNRI — Milestone Plan

**Version:** 1.0 | **Date:** 23 Feb 2026

> This plan is designed so anyone can understand it at a glance.

---

## The Journey in One Picture

```
  YOU ARE HERE
       |
       v
  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
  │  MONTH   │    │ MONTH   │    │ MONTH   │    │ MONTH   │    │ MONTH   │
  │   1      │───▶│  2-3    │───▶│  4-5    │───▶│  6-9    │───▶│  10+    │
  │          │    │         │    │         │    │         │    │         │
  │ PROVE IT │    │BUILD IT │    │GROW IT  │    │EARN IT  │    │SCALE IT │
  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
   1 country      4 countries    7 countries    Revenue        Top 20
   1 guide        Auto pipeline  2 new tabs     $10K/month     countries
   100 users      $500/month     Starter Kits   WhatsApp Pro   $30K+/month
```

---

## Explained for Everyone

### If You're 5 Years Old

> Imagine your uncle lives in another country. He has to follow rules from TWO places — India AND the country he lives in. But the rules are written in boring grown-up language and hidden on confusing websites.
>
> SmartNRI is like a helpful friend who reads all the boring stuff every day and tells your uncle: "Hey! This rule changed. Here's what it means. Here's where to check."
>
> First we help uncles in 1 country. Then 4. Then 7. Then everywhere.

### If You're 15 Years Old

> 18 million Indians live abroad and they all struggle with the same thing: understanding government rules in two countries at once. Tax, visas, bank accounts, property.
>
> SmartNRI uses AI to automatically read government websites every day, summarize the important changes into 3-bullet cards, and publish them on a simple website — with a direct link to prove every fact.
>
> It starts small (1 guide, 1 country), grows to 7 countries with automated daily updates, then makes money through affiliate links and paid starter kits — without ever selling financial products or putting content behind a paywall.

### If You're 30 Years Old

> SmartNRI is a fully autonomous intelligence pipeline that scrapes Tier 1 government sources across 7 NRI-heavy countries, runs content through an LLM with Source Match validation (every summary includes a verifiable quote from the source document), and publishes per-country static HTML pages.
>
> Monetization: contextual affiliates (Wise, ClearTax), digital starter kits ($29-49), Pro WhatsApp digest ($5/month), and B2B sponsored verified cards ($500-2K/month). All content free, forever.
>
> Unit economics: $30/month infrastructure. Break-even at ~20 affiliate conversions. Positioned for acquisition by NRI fintechs at $2-5M within 24 months.

---

## Phase-by-Phase Detail

### PHASE 1: PROVE IT (Month 1)

**Goal:** Prove that NRIs want this. Zero infrastructure. Just content + distribution.

| Milestone | What It Means | How You Know It's Done |
|---|---|---|
| Write "Return to India" hero guide | 30-40 step checklist with source links for every step | Guide is published, every step has a .gov link |
| Sign up 3 affiliate partners | Wise, ClearTax NRI, NRI Legal Services | Affiliate links are live and trackable |
| Share in 5 WhatsApp groups | Post the guide in NRI communities you belong to | Guide has been shared, you can see responses |
| Get first 100 visitors | People actually click and read | Plausible Analytics shows 100+ unique visitors |
| UX: 50ms Trust Test | Hero section communicates authority instantly | "Verified against X sources across Y countries" visible in first viewport. No decorative fluff — authority signals only |

**Effort:** Solo founder. No code changes. Content + distribution only.
**Cost:** $9/month (Plausible Analytics) + domain cost.
**UX Design Principle:** GOV.UK clarity, not Apple beauty. If a stressed NRI on a phone in a Dubai metro can tell "this is legit" in under a second, the design is right.

---

### PHASE 1.5: BUILD IT (Months 2-3)

**Goal:** Automate the pipeline. Expand to 4 countries. Make it hands-free.

| Milestone | What It Means | How You Know It's Done |
|---|---|---|
| Country profiles created | JSON files for Malaysia, USA, Canada, Singapore + India GLOBAL | `countries/` directory has 5 JSON files, all valid |
| Pipeline runs multi-country | Scraper → Summarizer → Publisher works for all 4 countries | `python main.py` produces 4 country HTML files + global |
| Source Match validation live | Every card has a source quote + URL liveness check | Cards show "Source Quote" and "Last Verified" fields |
| Per-country HTML pages | `us.html`, `ca.html`, `sg.html`, `my.html` all generated | Each URL loads with country-specific + global content |
| Country switcher on site | Dropdown/tabs to switch between countries | User can switch countries, selection persists |
| GitHub Actions cron running | Pipeline triggers automatically every 24 hours | Daily commits to repo with updated HTML |
| First affiliate revenue | Someone clicks an affiliate link and converts | $1+ tracked in affiliate dashboard |
| UX: Cognitive Fluency | Cards are scannable in 3 seconds on mobile | Badge colour, "So What?" line, source link — all visible without scrolling a card |
| UX: Source Quote display | Every card shows the exact government quote | Source quote field + "Last Verified" timestamp visible on every card |

**Effort:** Solo founder + AI builder agent (Claude Code).
**Cost:** ~$30/month (hosting + API calls).

---

### PHASE 2: GROW IT (Months 4-5)

**Goal:** Add Gulf countries. Launch Guides and Compare tabs. First paid product.

| Milestone | What It Means | How You Know It's Done |
|---|---|---|
| UAE + Saudi Arabia sources live | Country profiles with MOHRE, ICA, Qiwa, Absher sources | Pipeline fetches and summarizes Gulf content |
| Arabic source handling | English summaries from Arabic government pages | LLM correctly translates/summarizes Arabic content |
| Hindi + Malayalam RED alerts | Urgent alerts translated for blue-collar Gulf NRIs | RED cards display in 3 languages |
| Guides tab live | Transition checklists published as interactive pages | At least 3 guides live: Return to India, Moving to UAE, NRI Property |
| Compare tab live | Side-by-side regulatory tables across countries | At least 3 comparison tables: Banking, Tax, Insurance |
| First Starter Kit sold | "UAE Starter Kit" ($39) published on Gumroad | At least 1 purchase |
| WhatsApp Channel (UAE) | Broadcast channel for UAE NRI updates | Channel created, first digest sent |
| UX: Clean End-States | Every guide/checklist ends with clear next actions | "Download as PDF" + "Share on WhatsApp" buttons on every guide and comparison table |
| UX: Compare table mobile | Comparison tables readable on phone | Card-based layout on mobile (not wide tables). Each row becomes a question-card with answers stacked |
| 1,000 monthly visitors | Organic + WhatsApp-driven traffic growing | Analytics confirms 1K+ uniques/month |

**Effort:** Solo founder + optional intern for source verification.
**Cost:** ~$100/month.

---

### PHASE 3: EARN FROM IT (Months 6-9)

**Goal:** Launch paid subscription. AI-powered Ask tab. Serious revenue.

| Milestone | What It Means | How You Know It's Done |
|---|---|---|
| SmartNRI Pro live ($5/month) | Daily WhatsApp digest + early alerts + priority Ask | Subscribers receiving daily messages |
| Ask tab functional | Users submit questions, AI finds verified answers | At least 50 answered questions published |
| Search Discoverer engine | Google Custom Search + LLM finds regulatory news automatically | Pipeline discovers items NOT in source list |
| Trend Sensor running | Google Trends + Reddit detect what NRIs are asking | Trending topics feed into discoverer |
| Critic LLM pass added | Second AI reviews every summary for accuracy | Hallucination detection rate measurable |
| 100 Pro subscribers | Recurring revenue from subscriptions | $500/month MRR from Pro alone |
| 10,000 monthly visitors | SEO + WhatsApp driving consistent traffic | Analytics confirms 10K+ uniques/month |
| $10K/month total revenue | Affiliates + Starter Kits + Pro combined | Revenue tracking confirms |

**Effort:** Solo founder + 1 part-time intern.
**Cost:** ~$500/month (WhatsApp API + infrastructure).

---

### PHASE 4: SCALE IT (Months 10+)

**Goal:** Expand to top 20 countries. Launch B2B. Position for acquisition.

| Milestone | What It Means | How You Know It's Done |
|---|---|---|
| 13+ countries live | Kuwait, Qatar, Oman, UK, Australia, + more | Country profiles created and pipeline running |
| Sponsored Verified Cards (B2B) | Banks/fintechs pay $500-2K/month for verified content slots | At least 3 paying B2B partners |
| Enterprise API | REST API for partners to embed SmartNRI data | API live with documentation, first integration |
| 100K monthly visitors | SEO authority established across NRI queries | Analytics confirms |
| $30K+/month revenue | All streams contributing | Revenue tracking confirms |
| Acquisition conversations | NRI fintechs expressing interest | Inbound inquiries or outreach responses |
| Content library: 500+ items | Guides, answered questions, comparison tables | Searchable, indexed content archive |

**Effort:** Small team (2-3 people).
**Cost:** ~$2K/month.

---

## The Numbers That Matter

| Metric | Month 1 | Month 3 | Month 6 | Month 12 |
|---|---|---|---|---|
| Countries live | 1 | 4 | 7 | 13+ |
| Monthly visitors | 100 | 1,000 | 10,000 | 100,000 |
| Published guides | 1 | 3 | 8 | 20+ |
| Monthly revenue | $0 | $500 | $5,000 | $30,000 |
| Founder hours/week | 10 | 5 | 3 | 3 |
| Team size | 1 | 1 | 1-2 | 2-3 |
| Monthly cost | $9 | $30 | $500 | $2,000 |

---

## One Rule Above All

> **Ship, then improve. Don't improve, then ship.**
>
> The first version will be imperfect. The guide won't cover everything.
> The design won't be beautiful. The pipeline will have bugs.
> That's fine. 100 NRIs reading an imperfect guide is worth more than
> 0 NRIs waiting for a perfect platform.
