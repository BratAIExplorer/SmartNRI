# SmartNRI — Agent Routing Logic

**Version:** 1.0 | **Date:** 21 Feb 2026

Every agent that receives a task on this project must first score the task using the formula below, then choose the appropriate framework and approach.

---

## Complexity Scoring Formula

```
Score = (Files Modified × 1.5) + (New Dependencies × 2) + Security Risk (1–5)
```

| Score | Tier | Recommended Approach |
|---|---|---|
| 1–3 | Simple | **Oat UI / Direct Edit** — Single file change, no logic |
| 4–6 | Moderate | **Scripted** — Python/JS script with error handling |
| 7–9 | Complex | **Multi-step with tests** — Write, run, verify, fix loop |
| 10+ | Critical | **Multi-agent review** — One agent builds, second audits before deploy |

---

## Task Type → Routing Guide

| Task Type | Example | Score | Approach |
|---|---|---|---|
| UI text/style update | Change a badge colour or card copy | 1–2 | Direct HTML edit |
| Add a new content card | New weekly update | 2–3 | `builder.py` injection |
| Add a new scraper source | New Tier 1 gov site | 4–6 | Python scripted, test first |
| Change LLM prompt | Refine "So What?" summary | 3–5 | Update `summarizer.py`, dry-run |
| VPS config change | New Nginx rule or port | 6–8 | Stage first, audit before apply |
| Security change | API key rotation, `.env` update | 8–10 | Multi-agent review required |
| New phase feature | Add checklist or chatbot | 7–9 | Plan in `specs/` first, then build |

---

## Framework Selection

- **Phase 1 (Current):** All tasks use simple Python scripts (no orchestration framework). Claude/Antigravity writes them directly.
- **Phase 2+:** If logic becomes cyclic (retry loops, multi-source correlation), evaluate LangGraph.
- **Phase 4+:** If parallel agents are needed (e.g., Singapore + Malaysia simultaneously), evaluate CrewAI.

---

## Security Scan (Always Run Before Deploy)

```bash
# Check for accidentally hardcoded secrets
grep -rn "sk-" . --include="*.py" --include="*.js" --include="*.html"
grep -rn "AIza" . --include="*.py" --include="*.js"
grep -rn "Bearer " . --include="*.py"

# Check for PII in output files
grep -rn "@" output/ 
grep -rn "passport" output/ -i
```

If any of the above return hits, **STOP. Do not deploy. Fix the leak first.**

---

## The Audit Checklist (For Layer 3 Review)

Before marking any task complete, verify:

- [ ] Does the change follow `claude.md` Golden Rules?
- [ ] Is any sensitive info hardcoded? (Run security scan)
- [ ] Does the UI still load in under 2s?
- [ ] Does the watchdog still trigger correctly?
- [ ] Is `HANDOVER.md` updated with what was done?
- [ ] Is `state/system_state.json` updated with the new phase/module status?
