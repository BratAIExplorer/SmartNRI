# SmartNRI — Product Requirements

**Version:** 1.1 | **Phase:** 1 (Global NRI) | **Date:** 23 Feb 2026

---

## Problem Statement

Indian expats in Malaysia have no single, trustworthy, non-commercial reference for navigating the intersection of Malaysian government rules (Employment Pass, tax, driving licenses) and Indian government regulations (FEMA, NRE/NRO banking, ITR filing, OCI). Existing platforms (SBNRI, Vance) are transactional — they want to sell products. WhatsApp groups spread unverified claims. The result is confusion, missed deadlines, and compliance risk.

---

## Vision

SmartNRI is a fully autonomous, hands-free, government-verified reference platform for Indian expats. It is the **Independent Auditor in your pocket** — it does not sell, it only informs. Users verify for themselves using the direct source links provided with every item.

---

## Phase 1 Target Audience

- Primary: Indian expats worldwide — Malaysia, Singapore, UAE, UK, US, Australia
- Entry channel: WhatsApp sharing among trusted networks
- Day 1 Users: Founder's family, friends, and colleagues
- **Geo-capture:** Country of residence collected at registration to segment future content

---

## Non-Goals (Phase 1)

- No country-specific hero imagery (hero must work for any country)
- No live chatbot (placeholder UI only)
- No community forum
- No native mobile app
- No financial product sales or recommendations

---

## Core Features: Phase 1

### 1. The Daily Digest (Tab: "Today's Signal")
- 3–5 verified updates per day, auto-generated from Tier 1 government sources
- Each item includes:
  - Verification badge (GREEN/ORANGE/BLUE/RED)
  - One-line "So What?" summary (max 2 sentences)
  - Up to 3 action bullet points
  - Direct clickable link to the source document
  - Publication date
- Standard footer on every card: *"This is a reference guide. Verify with the linked official source before taking action."*
- Content refreshes automatically every 24 hours via the automation pipeline

### 2. The Compliance Checklist (Tab: "My Checklist")
- Static checklist, client-side only — no data sent to server
- Categories:
  - **Banking Compliance**: Account types (NRE/NRO/Resident), FEMA rules, nominee registration
  - **Document Reminders**: Document type (dropdown) + expiry date only. Reminder lead-time option (90/60/30 days).
  - **Investment Self-Audit**: PIS account, FATCA compliance, prohibited investments (PPF for NRIs, agricultural land)
  - **Joint Accounts**: Guidance on E or S vs "Jointly" for NRI accounts
- "No Change" shortcut on 6-month re-check (tap once to confirm no update needed)
- Privacy statement visible: *"We never store account numbers, document scans, or personal financial data. This checklist runs entirely in your browser."*

### 3. Ask + Trusted Voices (Tab: "Ask")
- Search bar placeholder (Phase 1: non-functional, shows "Coming Soon" on submit)
- Pre-populated Suggested Questions (6 chips as visual teaser)
- Trusted Voices section: Static curated grid of 6–8 recommended YouTube/Instagram channels
  - Links only, no content reproduction
  - Disclaimer: *"These are community recommendations. We do not reproduce or verify their content."*

---

## Content Calendar (Week 1 Launch)

| Day | Topic | Badge |
|---|---|---|
| Mon | Malaysia EP Salary Doubling (June 2026) | GREEN |
| Tue | India Budget 2026: 7 NRI Changes | GREEN |
| Wed | FEMA Wake-Up: Resident Account Risk | RED |
| Thu | NRE vs NRO vs FCNR Decision Guide | GREEN |
| Fri | The 120-Day Trap (Deemed Resident) | ORANGE |
| Sat | Myth Buster: Viral NRI Instagram Claim | BLUE |
| Sun | Weekly Digest Summary | GREEN |

---

## Registration Gate (Added v1.1)

- **Trigger:** Appears on first page load; also triggered when clicking Checklist or Ask tabs
- **Fields collected (all required):**
  - First Name
  - Email Address
  - Country of Residence (dropdown: Malaysia, Singapore, UAE, US, UK, AU, CA, DE, NZ, HK, JP, Other)
  - Role: Salaried Employee / Business Owner / Freelancer / Student / Retired / Other
- **Storage:** `localStorage` key `snri_user` (JSON) — no server-side call yet
- **Gate behaviour:**
  - Signal tab (first tab) is freely visible — acts as content teaser
  - Checklist and Ask tabs blocked until registered
  - Registration persists across sessions (localStorage)
- **Backend hook:** `fetch('/api/register', ...)` comment in script — ready to wire
- **Purpose:** Build email list, understand country distribution, segment by role

---

## Privacy Requirements

- Registration data stored in `localStorage` only until backend endpoint is wired
- No PII collected beyond name, email, country, role
- No cookies beyond session (no tracking)
- No analytics that identify individuals
- Checklist state lives in `localStorage` only — clears on browser reset
- Document reminders: type + expiry date only — no document upload, no number

---

## Performance Requirements

- Page must load under 2 seconds on a Malaysian 4G connection
- Total page weight: under 50KB (Oat UI ~8KB + custom CSS ~5KB + content)
- Must be fully functional with JavaScript disabled (content still readable)

---

## Monetization Roadmap (Phase 2+)

- Contextual affiliate links: When a checklist item is flagged (e.g., no NRO account), show a "Sponsored: Open NRO with [Bank Partner]" card
- Lead generation: Partner with verified CAs/tax firms specialising in Malaysia-India DTAA
- Exchanges: Affiliate links to Moomoo, Public Invest, Rakuten (Malaysia) and Zerodha, Groww (India)
- Premium tier (Phase 3+): Document expiry push notifications, personalised compliance scorecard

---

## Verification Framework (Mandatory)

Every published item MUST have a source. The source tier determines the badge:

| Tier | Badge | Example Source |
|---|---|---|
| Government circular (`gov.in` / `gov.my`) | 🟢 GREEN | esd.imi.gov.my/announcement |
| Reputable advisory (KPMG, law firm, ET) | 🟠 ORANGE | KPMG GMS Flash Alert |
| Trend-verified, cross-referenced | 🔵 BLUE | Reddit question + gov.in confirmation |
| Time-sensitive action required | 🔴 RED | FEMA violation risk |

If no Tier 1 source is found: **do not publish.** Log the item as `SKIPPED` in the pipeline.

---

## Accessibility & Compliance

- All interactive elements must have unique IDs for accessibility
- Alt text on all images (if any added in future)
- Disclaimer footer pinned to bottom of every tab
- No advice language ("you must", "you should") — only informational language ("the rule states", "the circular confirms")
