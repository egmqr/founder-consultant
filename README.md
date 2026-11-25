# founder-consultant

A product-agnostic AI agent skill that audits **the app or system you're building** (web app, API, mobile app, AI agent or automation) against a one-stop checklist for **robust, reliable and secure AI-built products**. It works with Claude Code, Codex, or any agent that reads `SKILL.md`.

## Features

- **Audits your actual project:** it reads your code, config and git history, not just a questionnaire.
- **Ranked findings:** each one comes with its check ID, file:line evidence, the risk in plain words, and the smallest fix.
- **Honest coverage:** it lists which checks passed, which don't apply and why, and which it couldn't verify.
- **Fixes on request:** only with your go-ahead, each with a test that fails on the old code. Authorization fixes get a test that calls the route as the wrong user.
- **Never ships for you:** no commits, pushes or deploys unless you ask.
- **Works on any stack:** checks are written so they apply to any language or framework.

## What it checks

<!-- kb-summary:start -->
Product-agnostic AI skill that audits the app or system you're building: data & knowledge ownership, server-side auth, secrets, agent harness, shadow AI, models, vendors, evidence & recovery, tenant isolation, change control, business viability, automation rollout, user trust. 108 checks in 13 areas (updated 2026-11-25).

- **Data and knowledge ownership (DATA)**
- **Server-side authorization (AUTHZ)**
- **Secrets (SEC)**
- **Agent harness (HAR)**
- **AI governance and shadow AI (GOV)**
- **Models and AI runtime (MOD)**
- **Vendors and AI agencies (VEN)**
- **Evidence and recoverability (EVI)**
- **Tenant isolation (TEN)**
- **Change control for in-house builders (CHG)**
- **Business viability (BIZ)**
- **Automation rollout (ROLL)**
- **User communication and trust (COM)**
<!-- kb-summary:end -->

Each area's checks, and how to verify them, are in [knowledge/checklist.md](knowledge/checklist.md).

## Install

```bash
git clone https://github.com/egmqr/founder-consultant.git
```

```bash
bash founder-consultant/setup.sh
```

`setup.sh` links the skill into `~/.claude/skills` and `~/.codex/skills` (a symlink, or a junction on Windows), so a `git pull` updates it. It then runs the self-test. It needs Python 3 and Bash (Git Bash on Windows). You can also copy the folder into your agent's skills directory by hand.

## Use it

> Use the founder-consultant skill to audit this project.

> Use founder-consultant to check only server-side authorization in ~/code/my-api.

## Layout

```
SKILL.md                  the agent's instructions
knowledge/checklist.md    the audit checklist
knowledge/insights/       why each check matters
scripts/kb.py             validates the checklist and rebuilds the summaries
setup.sh                  install
```

## License

[MIT](LICENSE)
