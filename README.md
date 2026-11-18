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
Product-agnostic AI skill that audits the app or system you're building against a checklist covering data ownership, server-side authorization, secrets, agent harness, vendors and AI agencies, evidence and recoverability, user communication and trust. 23 checks in 7 areas (updated 2026-11-19).

**Data ownership (DATA)**
- `DATA-1` Every record that matters lives in a server database you own.
- `DATA-2` No business logic reads a browser-only value that the server doesn't also hold.
- `DATA-3` Automatic backups exist, and a restore has actually been done and dated.

**Server-side authorization (AUTHZ)**
- `AUTHZ-1` Every API route checks who is calling on the server (token, session, signed URL), on every request.
- `AUTHZ-2` Every route checks what the caller may do: role, plus ownership of the specific record (account, customer, event).
- `AUTHZ-3` Hiding a button is not access control.
- `AUTHZ-4` Tests call each route directly as the wrong user (no token, other customer, lower role) and expect a refusal.

**Secrets (SEC)**
- `SEC-1` No secret key ships in front-end code or browser bundles.
- `SEC-2` Scan the code and its full git history for keys; rotate every key that was ever exposed, even once.
- `SEC-3` Secrets live in server environment variables or a secrets manager; third-party calls (payments, email, AI providers) go through your server.

**Agent harness (HAR)**
- `HAR-1` Your standards for AI agents are written down in files you own and version: rules, project knowledge, allowed tools.
- `HAR-2` What each agent may touch is explicit (permissions, protected paths, no-go actions), and enforced rather than just requested.
- `HAR-3` Work is proven by checks (tests, builds, contract checks) before anything ships; agents report what they did not verify.
- `HAR-4` Swapping a model or tool is a config change, not a rebuild.

**Vendors and AI agencies (VEN)**
- `VEN-1` Ask every AI vendor what they did before.
- `VEN-2` Talk to a customer who has worked with them for more than a year before signing.
- `VEN-3` Know who patches, monitors and supports the agent in year two and during an outage, and give vendors least-privilege access with their own credentials.

**Evidence and recoverability (EVI)**
- `EVI-1` Keep a dated register of every AI system and automation: what it does, the data it touches, who built it, who owns it now, and the last independent review with its reviewer.
- `EVI-2` Access is provable: 2FA on every account, no shared passwords, agents on their own service credentials.
- `EVI-3` Logging and retention are confirmed per system, and a one-page incident and recovery summary records the date and result of the last drill.

**User communication and trust (COM)**
- `COM-1` The product delivers its core value up front; it doesn't hide it behind engagement tricks (forced follows, "reply with a keyword", fake urgency or other dark patterns).
- `COM-2` Conversations with users stay real: AI or automated replies are labelled as automated and can hand off to a person.
- `COM-3` Abuse is handled without feeding it: users can block and report, and admins can hide or remove bad-faith content quickly.

Why each check matters:

- [R001](knowledge/insights/R001.md) Own your agent harness instead of rebuilding it
- [R002](knowledge/insights/R002.md) Vet AI agencies with one question
- [R003](knowledge/insights/R003.md) Real conversations beat engagement tricks
- [R004](knowledge/insights/R004.md) Move data, permissions and keys off the browser
- [R005](knowledge/insights/R005.md) Looking done is not being done
- [R006](knowledge/insights/R006.md) Build the AI evidence file before the insurer asks
<!-- kb-summary:end -->

The full list, with how to verify each check, is in [knowledge/checklist.md](knowledge/checklist.md). The short version for anyone shipping an AI-built app:

1. **Data** lives in a server database you own, with tested restores. The browser only caches.
2. **Permissions** are checked on the server for every route (identity, role and record ownership), and tests prove the wrong user is refused.
3. **Secrets** never reach the browser or git history; anything ever exposed is rotated.
4. **Agents** work inside a harness you own: written rules, explicit permissions, and checks before shipping.
5. **Vendors** have a track record and a year-two support plan, with least-privilege access.
6. **Evidence:** a register of AI systems, provable access control and a dated recovery drill.

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
