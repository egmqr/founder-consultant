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
Product-agnostic AI skill that audits the app or system you're building against a checklist covering data and knowledge ownership, server-side authorization, secrets, agent harness, AI governance and shadow AI, models and AI runtime, vendors and AI agencies, evidence and recoverability and more. 70 checks in 13 areas (updated 2026-11-19).

**Data and knowledge ownership (DATA)**
- `DATA-1` Every record that matters lives in a server database you own.
- `DATA-2` No business logic reads a browser-only value that the server doesn't also hold.
- `DATA-3` Automatic backups exist, and a restore has actually been done and dated.
- `DATA-4` Business knowledge AI relies on (pricing, policies, playbooks, decisions, customer history, expert judgment, prompts and example sets) lives in plain, versioned files or stores the business owns, one topic per file, with drafts kept apart from decisions, so a model or vendor switch keeps it.
- `DATA-5` No bulk export of company or customer data to a third party (for training, licensing or "AI insights") happens without a written decision on what is being sold, its value and the contract terms.
- `DATA-6` Imported or migrated records carry their originating system, original ID and import date.

**Server-side authorization (AUTHZ)**
- `AUTHZ-1` Every API route checks who is calling on the server (token, session, signed URL), on every request.
- `AUTHZ-2` Every route checks what the caller may do: role, plus ownership of the specific record (account, customer, event).
- `AUTHZ-3` Hiding a button is not access control.
- `AUTHZ-4` Tests call each route directly as the wrong user (no token, other customer, lower role) and expect a refusal.
- `AUTHZ-5` Sensitive actions (payments, payout or bank-detail changes, account recovery, bulk exports) require step-up verification even for a signed-in user.

**Secrets (SEC)**
- `SEC-1` No secret key ships in front-end code or browser bundles.
- `SEC-2` Scan the code and its full git history for keys; rotate every key that was ever exposed, even once.
- `SEC-3` Secrets live in server environment variables or a secrets manager; third-party calls (payments, email, AI providers) go through your server.
- `SEC-4` Every credential is short-lived and scoped to one job; there are no long-lived or shared keys.
- `SEC-5` Dependencies, runtimes and model versions are pinned (with checksums for downloaded weights), and updates go through review and tests before deploy.
- `SEC-6` An inventory of every internet-reachable host, service and file share exists with its last patch date, and anything unpatched or unneeded is closed.

**Agent harness (HAR)**
- `HAR-1` Your standards for AI agents are written down in files you own and version, starting with one short rules file at the repo root that every agent loads at session start.
- `HAR-2` What each agent may touch is explicit (permissions, protected paths, no-go actions), and enforced rather than just requested.
- `HAR-3` Work is proven by checks (tests, builds, contract checks) before anything ships; agents report what they did not verify.
- `HAR-4` Swapping a model or tool is a config change, not a rebuild.
- `HAR-5` Agents get a one-page map of the codebase, not the whole library: what each folder holds, where data is stored, and which areas are off limits.
- `HAR-6` One check script runs tests, type checks, linting and a dependency scan, and no task counts as done until it passes and its output is in the summary.
- `HAR-7` Every agent has its own identity and a named human owner, and agents or integrations unused for 30 days are retired with their keys revoked.
- `HAR-8` A kill switch exists and has been drilled: one documented command revokes agent credentials, disables scheduled agent jobs and stops running ones.
- `HAR-9` Every AI provider account has daily and monthly spend caps, and agent calls are rate-limited.
- `HAR-10` Every agent action (what it sent, changed or deleted) is logged to storage the business controls, with the steps to reverse it.
- `HAR-11` Corrected or rejected agent outputs are logged (task, output, what was expected, who caught it), and repeated failures become rules.

**AI governance and shadow AI (GOV)**
- `GOV-1` An inventory lists every AI tool and account used with company data, with owner and plan type; personal accounts used for work are moved to company plans.
- `GOV-2` Staff have a sanctioned AI front door: company AI chat behind single sign-on, provisioned and removed with the staff directory, and client or financial data only goes to models whose terms forbid training on it.
- `GOV-3` Actual staff AI use is measured and compared with the sanctioned tools at least quarterly.
- `GOV-4` Third-party app grants on the company identity and office suite are reviewed on a schedule; unused or over-scoped grants are revoked.

**Models and AI runtime (MOD)**
- `MOD-1` All model calls go through one layer the business controls (gateway or router) that routes by data class: private or customer data only goes to models you control or whose terms you accept.
- `MOD-2` Each model was chosen by running the real task on several candidates and keeping the smallest that passes, and new models face misuse probes before adoption.
- `MOD-3` Changing facts (prices, policies, specs) come from a maintained document store at answer time, not from fine-tuning; any fine-tuned model beat its base model on a held-out evaluation.
- `MOD-4` Self-hosted models listen only on a private network behind an authenticating gateway, with no public port or domain.
- `MOD-5` Agents and self-hosted models run contained: networking off by default with an allowlist, a non-admin user, a read-only filesystem with one scratch directory, and their own action log.
- `MOD-6` Weights, fine-tuning data, runtime config and keys for self-hosted models live in storage you own, and moving to another host is a scripted, tested procedure.
- `MOD-7` The hosting choice (vendor API, rented servers or owned hardware) is written down with a measured trial of the target model on the real workload and a memory estimate.
- `MOD-8` A license register covers every model in use: attribution, revenue or user caps, and use restrictions.
- `MOD-9` Each AI provider has a written exit plan: which jobs it runs, where the data lives, how to export it, and the fallback.
- `MOD-10` Latency-sensitive AI (voice, live chat) streams every stage and has a measured end-to-end latency budget.

**Vendors and AI agencies (VEN)**
- `VEN-1` Ask every AI vendor what they did before.
- `VEN-2` Talk to a customer who has worked with them for more than a year before signing.
- `VEN-3` Know who patches, monitors and supports the agent in year two and during an outage, and give vendors least-privilege access with their own credentials.
- `VEN-4` Any vendor-built system survives firing the vendor: code, hosting, domains, databases and model or API accounts are owned by the business, which can run, deploy and change it with the vendor's access revoked.
- `VEN-5` Before any vendor, consultant or AI tool connects to email, file storage or the CRM, a written note states what data it reads, where the data goes, and who signed off.
- `VEN-6` A system inventory lists every third-party tool with owner, workflow, data held and export path, and seats unused for 60 days are removed.

**Evidence and recoverability (EVI)**
- `EVI-1` Keep a dated register of every AI system and automation: what it does, the data it touches, who built it, who owns it now, and the last independent review with its reviewer.
- `EVI-2` Access is provable: 2FA on every account, no shared passwords, agents on their own service credentials.
- `EVI-3` Logging and retention are confirmed per system, and a one-page incident and recovery summary records the date and result of the last drill.
- `EVI-4` You know what your business insurance says about AI, and what the insurer would need to see to cover it; the evidence file is built to that list.

**Tenant isolation (TEN)**
- `TEN-1` The tenant model is chosen on purpose and written down: a separate database or stack per customer, or shared tables where every row carries a customer ID.
- `TEN-2` Isolation is enforced below the app: database row-level security or separate credentials per customer, so a query without the right customer context returns nothing even when the code is wrong.
- `TEN-3` Every release runs automated cross-tenant attacks: sign in as one test customer and try to read, change and export another customer's data through every screen and API (changed IDs, direct API calls, exports).

**Change control for in-house builders (CHG)**
- `CHG-1` Every tool or automation staff build lives in one company repository under company accounts with 2FA, never on a personal laptop or account, so the tool stays when the person leaves.
- `CHG-2` Builders work against realistic sample data generated from the real schema (no real names, numbers or addresses); real data stays behind review.
- `CHG-3` The main branch is protected: every change goes through a pull request with automatic secret scanning and one named reviewer, and every release logs who approved it.
- `CHG-4` AI-generated code is marked in commit or pull-request metadata, and each such change has a named human owner.
- `CHG-5` A written list names who may build AI tools and automations and the sanctioned environment for each.

**Business viability (BIZ)**
- `BIZ-1` Someone is paying, or has committed to pay, for the problem this product solves.
- `BIZ-2` The product answers "why wouldn't the customer build this themselves with the same AI tools?": it saves them time, brings engineering they don't have, or takes accountability when it breaks.
- `BIZ-3` An independent security and production-readiness review is done before the first paying customer signs.

**Automation rollout (ROLL)**
- `ROLL-1` A process is written down (including manual checks and unwritten know-how) and its data cleaned before it is automated.
- `ROLL-2` The first automation is chosen with a written rationale: a foundation others depend on, a fixed deadline, or measurable proof.
- `ROLL-3` A new automated process replaces the old one only after a shadow run on live data with daily comparison.
- `ROLL-4` Every AI rollout names the workflow it changes, with baseline and after measurements (hours, error rate, cycle time) rather than seat counts.

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
- [R007](knowledge/insights/R007.md) A prompt asks; a harness makes it behave
- [R008](knowledge/insights/R008.md) Be the easiest business to insure
- [R009](knowledge/insights/R009.md) Give in-house builders a door, not a back window
- [R010](knowledge/insights/R010.md) Keeping customers apart is the product
- [R011](knowledge/insights/R011.md) Your real competitor is the customer who can build it
- [R012](knowledge/insights/R012.md) Make every built system survive firing the vendor
- [R013](knowledge/insights/R013.md) Keep AI knowledge in owned, conflict-free files
- [R014](knowledge/insights/R014.md) Give staff a sanctioned AI front door
- [R015](knowledge/insights/R015.md) Buy AI hardware only for proven reasons
- [R016](knowledge/insights/R016.md) Prove demand with paying customers before fundraising
- [R017](knowledge/insights/R017.md) Capture know-how in files before switching models
- [R018](knowledge/insights/R018.md) Treat commission-paid AI recommendations as sales
- [R019](knowledge/insights/R019.md) Choose the first automation by foundation, deadline, proof
- [R020](knowledge/insights/R020.md) Business AI plans don't cover personal accounts
- [R021](knowledge/insights/R021.md) Stream every stage to cut voice lag
- [R022](knowledge/insights/R022.md) Count and revoke third-party app grants
- [R023](knowledge/insights/R023.md) Plan a phased exit from vendor AI
- [R024](knowledge/insights/R024.md) Lock down self-hosted models behind a gateway
- [R025](knowledge/insights/R025.md) Control the model layer even when renting
- [R026](knowledge/insights/R026.md) Buy commodities; own your decision logic layer
- [R027](knowledge/insights/R027.md) Harden an internal tool before selling it
- [R028](knowledge/insights/R028.md) Contain models whose makers report nothing
- [R029](knowledge/insights/R029.md) Own the model stack, rent the hardware
- [R030](knowledge/insights/R030.md) Most agent breaches are key-handling failures
- [R031](knowledge/insights/R031.md) Size the model first, then the hardware
- [R032](knowledge/insights/R032.md) Own the memory your AI relies on
- [R033](knowledge/insights/R033.md) Route each job to the right model
- [R034](knowledge/insights/R034.md) Scope agent jobs, approve actions, end access
- [R035](knowledge/insights/R035.md) Give every agent an identity and owner
- [R036](knowledge/insights/R036.md) Fix the process before you automate it
- [R037](knowledge/insights/R037.md) Audit every change; AI attackers move faster
- [R038](knowledge/insights/R038.md) Seal the agent sandbox - network, rights, keys
- [R039](knowledge/insights/R039.md) Inventory every system before rebuilding with AI
- [R040](knowledge/insights/R040.md) Let the job pick the model and hardware
- [R041](knowledge/insights/R041.md) Keep model, data and exit decisions yourself
- [R042](knowledge/insights/R042.md) Start from recent data, cut over after shadowing
- [R043](knowledge/insights/R043.md) Measure AI by workflow outcomes, not seats
- [R044](knowledge/insights/R044.md) Capture your experts' judgment in owned systems
- [R045](knowledge/insights/R045.md) Log agent failures and turn repeats into rules
- [R046](knowledge/insights/R046.md) Tune for behavior; keep knowledge in documents
- [R047](knowledge/insights/R047.md) Assume shipped code can be read
- [R048](knowledge/insights/R048.md) Know what you sell before exporting data
- [R049](knowledge/insights/R049.md) Let a paying pilot customer fund the build
- [R050](knowledge/insights/R050.md) Build and drill an agent kill switch
- [R051](knowledge/insights/R051.md) Get sign-off before connecting AI to email
- [R052](knowledge/insights/R052.md) Build your expertise into an engine you own
- [R053](knowledge/insights/R053.md) Find and fix shadow AI accounts
- [R054](knowledge/insights/R054.md) AI writes code; a named human owns it
<!-- kb-summary:end -->

The full list, with how to verify each check, is in [knowledge/checklist.md](knowledge/checklist.md). The short version for anyone shipping an AI-built app:

1. **Data and knowledge** live in systems you own, with tested restores. The browser only caches, and the know-how your AI uses is in versioned files, not trapped in a vendor.
2. **Permissions** are checked on the server for every route (identity, role and record ownership), sensitive actions need step-up verification, and tests prove the wrong user is refused.
3. **Secrets** never reach the browser, shipped apps or git history; credentials are short-lived and scoped; dependencies are pinned; exposed hosts are inventoried and patched.
4. **Agents** work inside a harness you own: written rules, a codebase map, one check script, scoped permissions, a named owner, spend caps, action logs and a drilled kill switch.
5. **AI governance:** staff use a sanctioned AI front door, shadow AI accounts and app grants are found and cleaned up.
6. **Models** sit behind a gateway you control, are picked by evaluation, run contained, and each provider has an exit plan.
7. **Vendors** have a track record, the business owns every account they touch, and the system survives firing them.
8. **Evidence:** a register of AI systems, provable access control, a dated recovery drill, and what your insurer needs to see.
9. **Tenants** are kept apart below the app and attacked by tests on every release.
10. **Change control:** one company repo, sample data for building, protected main branch, named human owners for AI-written code.
11. **Business and rollout:** paying customers first, an independent review before launch, processes fixed before they're automated, and outcomes measured against a baseline.
12. **Trust:** no engagement tricks, automated replies are labelled, and abuse can be handled.

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
