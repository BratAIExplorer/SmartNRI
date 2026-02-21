# SmartNRI — Handover Protocol

**Version:** 1.0 | **Date:** 21 Feb 2026

This file defines the rules for agent handover. Every agent — Claude, Antigravity, or ChatGPT — MUST follow this protocol before ending a session, especially when credits are low or a session is switching between AI tools.

---

## Why This Exists

When you switch between AI agents mid-project, context is lost. The agent starting fresh has no memory of what was decided, what was built, or what was broken. This file is the **lifeboat** that prevents that loss.

---

## The 3-Agent Role Framework

| Role | Agent | Responsibility |
|---|---|---|
| **Architect** (Layer 1) | Antigravity / Gemini | Strategy, specs, architecture. Writes `specs/` docs. Does NOT write code. |
| **Builder** (Layer 2) | Claude Code | Implementation. Reads `specs/`, writes code, tests it, updates `HANDOVER.md`. |
| **Auditor** (Layer 3) | Antigravity or ChatGPT | Reviews Builder's output. Checks against `specs/architecture.md`. Approves or lists errors. |

---

## Handover Entry Template

When your session ends, **append** the following block to `HANDOVER.md`:

```markdown
---
### 🔄 Session Handover — [DATE TIME]
- **Last Active Agent:** [e.g., Antigravity / Claude 3.5 Sonnet]
- **Role:** [Architect / Builder / Auditor]
- **Session Goal:** [What you set out to do]
- **Completed:** [Bullet list of what was done]
- **Files Modified/Created:**
  - `[filename]` — [what changed]
- **Where I Left Off:** [Exact description of the blocker or stopping point]
- **Next Step for Next Agent:** [Clear, actionable instruction]
- **Critical Context:** [VPS port, env var name, API quirk, or key decision made]
- **State Updated:** [Yes/No — did you update system_state.json?]
---
```

---

## Critical Memory Rules (Always Include These)

Every handover MUST remind the next agent of these permanent facts:

> ⚠️ **VPS Rule:** SmartNRI runs in an isolated Docker container. Container name: `smartnri_app`. Port: `8085` (internal). Do NOT connect to other project containers or databases.

> ⚠️ **No PII:** Never store account numbers, passport scans, or personal financial data. Checklist data is client-side only.

> ⚠️ **No React:** Phase 1 uses Oat UI + custom CSS only. Do NOT introduce npm, webpack, or React.

> ⚠️ **No Social Scraping:** Do NOT scrape Instagram or YouTube content. Use public trend APIs only.

> ⚠️ **Secrets in .env:** API keys live in `/data/smartnri/.env`. Never hardcode. Never commit `.env` to git.

---

## Switching Agents: Step-by-Step

### When switching FROM Claude TO Antigravity:
1. Claude appends a handover entry to `HANDOVER.md`
2. Claude updates `state/system_state.json` with current module status
3. You (Founder) open a new Antigravity session
4. Paste this prompt:
   > "Read `HANDOVER.md` and `state/system_state.json` in the SmartNRI project. You are the Layer 3 Auditor. Review what Claude built. Check against `specs/architecture.md`. List any issues or approve."

### When switching FROM Antigravity TO Claude:
1. Antigravity appends a handover entry to `HANDOVER.md`
2. You (Founder) open Claude Code
3. Paste this prompt:
   > "Read `claude.md` and `HANDOVER.md` in the SmartNRI project. You are the Layer 2 Builder. The next task is listed in the handover. Build it, test it, then update `HANDOVER.md` with what you did."

---

## "Credit Low" Emergency Protocol

If you notice credits running low mid-task:

1. **Save your progress immediately** — don't start a new feature
2. Write a handover entry describing **exactly** where you are in the current task (line number, file, or error message)
3. Open the state file and mark the current task as `in_progress`
4. The next agent picks up from that exact point
