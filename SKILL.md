---
name: founder-consultant
description: Product-agnostic audit of what you're building (web app, API, mobile app, agent or automation) against a checklist for robust, reliable, secure AI products, covering data and knowledge ownership, server-side authorization, secrets, agent harness, AI governance and shadow AI, models and AI runtime, vendors and AI agencies, evidence and recoverability, tenant isolation, change control for in-house builders, business viability, automation rollout, user communication and trust. Use to audit the current project or system and get ranked findings with fixes. 93 checks in 13 areas (updated 2026-11-22).
---

# Founder consultant

A product-agnostic audit of whatever the user is building: web app, API, mobile app, AI agent, automation or the system around them. It checks the project against the numbered checklist in `knowledge/checklist.md` and reports ranked findings, each with the smallest fix. `knowledge/insights/` explains why each check matters.

`$SKILL` below is this skill's folder.

## Session start

```bash
python "$SKILL/scripts/kb.py" session start
```

This validates the checklist and refreshes the summaries. Read `knowledge/checklist.md` before doing anything else.

## Audit what the user is building

1. **Find the project.** By default it's the current working directory, or the path the user names. Learn what it is: stack, entry points, where data is stored, how users sign in, what calls third parties, and which AI agents or automations act on it. Read its own agent rules (AGENTS.md, CLAUDE.md, CONTRIBUTING).
2. **Pick the checks.** Choose every check whose area exists in the project. Skip one only when it can't apply (no browser, no API, no vendors), and say why.
3. **Run each check** the way its "Verify" step says, with evidence from the actual code, config and git history. A missing check is not proof of safety.
4. **Report** the findings ranked by severity. Each gets its check ID, file:line evidence, the risk in plain words, and the smallest fix. List the checks that passed and the ones you couldn't verify.
5. **Fix only with the user's go-ahead.** Make the smallest complete change and add a test that fails on the old code (for authorization: call the route as the wrong user and expect a refusal). Run the project's full test suite. Never commit, push or deploy unless the user asks.

## Session end

```bash
python "$SKILL/scripts/kb.py" session end
```

## Never

- Write audit results or details of an audited project into this skill's folder. Findings go to the user.
- Echo secrets, customer data or internal hostnames found during the audit; say where they are instead.
