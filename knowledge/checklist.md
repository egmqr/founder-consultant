# Audit checklist

The one-stop list this skill audits against. Every check has a stable ID, the insight(s) it came from, and how to verify it. New insights add or sharpen checks here; never renumber an existing ID.

Format rule (the summary script counts these): each check is one line starting with `- **AREA-N**`.

## Data and knowledge ownership (DATA)
<!-- short: data & knowledge ownership -->

- **DATA-1** Every record that matters lives in a server database you own. Browser storage (localStorage, sessionStorage, IndexedDB, cookies) is only a cache or a draft. Verify: list every browser-storage key and confirm that each one is either disposable UI state or a copy of a server record. _From R004, R005._
- **DATA-2** No business logic reads a browser-only value that the server doesn't also hold. Old cache keys that nothing writes anymore are the classic trap: results then differ by device. Verify: for each storage key, find its writers; a key that's read but never written is a bug. _From R004, R005._
- **DATA-3** Automatic backups exist, and a restore has actually been done and dated. Verify: name the last restore drill and its result. _From R004, R006._
- **DATA-4** Business knowledge AI relies on (pricing, policies, playbooks, decisions, customer history, expert judgment, prompts and example sets) lives in plain, versioned files or stores the business owns, one topic per file, with drafts kept apart from decisions, so a model or vendor switch keeps it. Verify: find where agent context and memory come from and who owns that storage. This includes memory AI tools build on their own (profiles, preferences, relationship graphs): confirm it can be exported in a usable format, and test the export. _From R013, R017, R032, R044, R052._
- **DATA-5** No bulk export of company or customer data to a third party (for training, licensing or "AI insights") happens without a written decision on what is being sold, its value and the contract terms. Verify: list outbound data feeds and their approvals. _From R048._
- **DATA-6** Imported or migrated records carry their originating system, original ID and import date. Verify: sample records in the new system. _From R042._
- **DATA-7** Any dataset built from operational records for fine-tuning or retrieval comes from a repeatable script that removes or masks personal and confidential fields and logs which records and systems went in. Verify: rerun the script and inspect its output and log. _From R064._

## Server-side authorization (AUTHZ)
<!-- short: server-side auth -->

- **AUTHZ-1** Every API route checks who is calling on the server (token, session, signed URL), on every request. Verify: list every route with its auth check; public routes are listed on purpose with what they expose. Internal, admin and localhost-only tools count as routes too; none is exempt because it isn't meant to face the internet. _From R004, R005, R059._
- **AUTHZ-2** Every route checks what the caller may do: role, plus ownership of the specific record (account, customer, event). Changing an ID in the request must never reach someone else's data (IDOR). Elevated actions read the caller's current role from the database on each request, not a role baked into a token, so a demoted admin's existing token is refused at once. _From R004, R005, R056._
- **AUTHZ-3** Hiding a button is not access control. Any action the UI hides must also be refused by the server. _From R004, R005._
- **AUTHZ-4** Tests call each route directly as the wrong user (no token, other customer, lower role) and expect a refusal. Verify: such a test exists per protected route and fails on code without the check. _From R004._
- **AUTHZ-5** Sensitive actions (payments, payout or bank-detail changes, account recovery, bulk exports) require step-up verification even for a signed-in user. Verify: try each action with only an existing session. _From R011._
- **AUTHZ-6** Access tokens expire in minutes, not days; refresh tokens are HttpOnly cookies rotated on every use; replaying a used refresh token revokes the whole session; and a password change ends existing sessions. Verify: replay an old refresh token and change a test user's password, then retry the old tokens. _From R056._
- **AUTHZ-7** Every API's CORS policy is a fixed allowlist of the product's own origins: no wildcard on routes returning private data, credentials only for listed origins, and the request's Origin never echoed back blindly. Verify: send requests with a foreign Origin header and read the response headers. _From R062._
- **AUTHZ-8** Every inbound webhook (payments, source control, auth and other providers) verifies the provider's signature with the endpoint secret before acting, and processed event IDs are stored so a replayed event is rejected. Verify: list every webhook route, send one unsigned and one replayed signed event, and expect both refused. _From R067._
- **AUTHZ-9** Passwordless sign-in links expire within minutes and work once, any post-login redirect target is checked against an allowlist of the product's own domains, and link requests are rate-limited per address and per IP. Verify: reuse a used link, wait past expiry, set the redirect to a foreign domain, and request links in a burst. _From R068._

## Secrets (SEC)
<!-- short: secrets -->

- **SEC-1** No secret key ships in front-end code or browser bundles. Know which keys are public by design (for example Firebase web API keys, publishable payment keys) and make sure server rules protect the data behind them. This includes mobile apps and firmware: inspect the real release artifacts, not just the source. _From R004, R005, R047._
- **SEC-2** Scan the code and its full git history for keys; rotate every key that was ever exposed, even once. After rotating, purge the secret from history and add a pre-commit secret scan; the scan also covers screenshots, logs and data dumps that AI tools committed, and each repository's public or private setting is confirmed. _From R004, R034, R060._
- **SEC-3** Secrets live in server environment variables or a secrets manager; third-party calls (payments, email, AI providers) go through your server. Keys sit in a vault you control, not only in a host's environment settings. Environment files are ignored and were never tracked; check the history of those paths. _From R004, R005, R030._
- **SEC-4** Every credential is short-lived and scoped to one job; there are no long-lived or shared keys. Verify: export keys and tokens with their age and scope. _From R030, R034, R038._
- **SEC-5** Dependencies, runtimes and model versions are pinned (with checksums for downloaded weights), and updates go through review and tests before deploy. Verify: lockfiles, pinned images and weight checksums. Infrastructure services (caches, databases, queues) are pinned to exact versions in deploy config, never a floating tag. _From R024, R030, R069._
- **SEC-6** An inventory of every internet-reachable host, service and file share exists with its last patch date, and anything unpatched or unneeded is closed. Verify: compare the inventory with an external scan. Include every cloud storage bucket with its public-access setting, and keep admin panels, database consoles and hosting control panels reachable only through a VPN or address allowlist, with two-factor login. _From R037, R057, R061._
- **SEC-7** Only buckets holding intentionally public assets allow public reads; uploads, backups, exports and config sit in private buckets served through expiring signed URLs, with access logging and alerts on unusual downloads. Verify: list buckets with their access policy and try an anonymous read. _From R057._
- **SEC-8** Services are network-segmented so each reaches only the peers it needs (a public-facing tool can't reach the database), every internal call is authenticated (service tokens or mutual TLS), and each service account has only the rights it uses. Verify: from a public-facing service, try to connect to the database and other internal services. _From R058._
- **SEC-9** Development and internal services bind to the loopback address unless they must be shared, and reject requests whose Host header isn't on an expected list, which blocks DNS-rebinding attacks. Verify: search server configs for 0.0.0.0 bindings and send a request with a foreign Host header. _From R059._
- **SEC-10** Public traffic passes a web application firewall with a maintained rule set in blocking mode on every route that takes user input (a reverse proxy alone only routes), repeat offenders are banned automatically, and spikes in blocks or bans raise an alert. Verify: send a harmless injection probe and confirm it is blocked, logged and counted toward an alert. _From R065._
- **SEC-11** Staff sign-in policies never trust network location alone: they require a verified compliant device (patched, protected, encrypted), step up or block on risky sign-ins, and apply stricter rules to admin consoles and sensitive data than to everyday tools. Verify: export the sign-in policies and test a sign-in from a non-compliant device and from a flagged location. _From R066._
- **SEC-12** Critical infrastructure components are reviewed at least yearly for maintenance health and license changes (including community forks that now receive the security fixes), and each sits behind one adapter so switching provider is a config change. Verify: the dated review and the number of files that import the client directly. _From R069._

## Agent harness (HAR)
<!-- short: agent harness -->

- **HAR-1** Your standards for AI agents are written down in files you own and version, starting with one short rules file at the repo root that every agent loads at session start. It covers stack, structure, naming and forbidden actions (touching production, deleting data, putting keys in code), and every rule is easy to check. It must work no matter which model is plugged in. New rules trace back to logged agent failures, so the file grows from real mistakes. _From R001, R007, R045._
- **HAR-2** What each agent may touch is explicit (permissions, protected paths, no-go actions), and enforced rather than just requested. Each agent has one written task scope; actions that move money, delete data or contact customers need explicit human approval. Agents that read untrusted input (email, web pages, documents) treat it as data and can't act on instructions inside it. The scope is written before deployment and names the points where the agent must stop and ask a human and how its output is verified; attempts outside it are blocked and logged. _From R001, R018, R034._
- **HAR-3** Work is proven by checks (tests, builds, contract checks) before anything ships; agents report what they did not verify. _From R001._
- **HAR-4** Swapping a model or tool is a config change, not a rebuild. If a new tool forces a rebuild, the standards weren't in the harness. Keep a model-per-job map you own, with a tested fallback model per task, and load agent memory from files you own. Self-hosted models expose the same request format as the hosted APIs they replace, so a move only changes an endpoint and model name in config. _From R001, R014, R029, R032, R041._
- **HAR-5** Agents get a one-page map of the codebase, not the whole library: what each folder holds, where data is stored, and which areas are off limits. It's updated on every merge and read before planning anything big. Verify: the map exists and matches the current tree. _From R007._
- **HAR-6** One check script runs tests, type checks, linting and a dependency scan, and no task counts as done until it passes and its output is in the summary. "Done" from an agent means confident, not verified. The script includes static security analysis, so every change, human- or agent-written, is scanned before merge. _From R007, R037._
- **HAR-7** Every agent has its own identity and a named human owner, and agents or integrations unused for 30 days are retired with their keys revoked. Verify: list agents with owner and last activity. _From R035._
- **HAR-8** A kill switch exists and has been drilled: one documented command revokes agent credentials, disables scheduled agent jobs and stops running ones. Verify: the date and result of the last drill. _From R035, R050._
- **HAR-9** Every AI provider account has daily and monthly spend caps, and agent calls are rate-limited. Verify: the caps in each provider console and the gateway config. _From R050._
- **HAR-10** Every agent action (what it sent, changed or deleted) is logged to storage the business controls, with the steps to reverse it. Verify: pick a logged action and reverse it. _From R035, R050._
- **HAR-11** Corrected or rejected agent outputs are logged (task, output, what was expected, who caught it), and repeated failures become rules. Verify: the failure log exists and recent rules link to entries in it. _From R045._
- **HAR-12** Files AI coding tools generate (screenshots, recordings, logs, traces, scratch output) go outside the repository or to ignored paths, and a pre-commit or CI check blocks committing images, recordings and debug dumps. Verify: try to commit a screenshot and check what the hook does. _From R060._

## AI governance and shadow AI (GOV)
<!-- short: shadow AI -->

- **GOV-1** An inventory lists every AI tool and account used with company data, with owner and plan type; personal accounts used for work are moved to company plans. Verify: compare the inventory with sign-in, expense and network data. _From R020, R053._
- **GOV-2** Staff have a sanctioned AI front door: company AI chat behind single sign-on, provisioned and removed with the staff directory, and client or financial data only goes to models whose terms forbid training on it. Verify: the sign-on config and the model terms. _From R014._
- **GOV-3** Actual staff AI use is measured and compared with the sanctioned tools at least quarterly. Verify: the latest comparison. _From R020._
- **GOV-4** Third-party app grants on the company identity and office suite are reviewed on a schedule; unused or over-scoped grants are revoked. Verify: export grants with scopes and last use. _From R022, R053._

## Models and AI runtime (MOD)
<!-- short: models -->

- **MOD-1** All model calls go through one layer the business controls (gateway or router) that routes by data class: private or customer data only goes to models you control or whose terms you accept. Verify: search the code for provider calls that bypass the gateway. Apps reach models only through one internal endpoint, and prompts that embed pricing rules, customer patterns or strategy count as private data. _From R025, R029, R033, R055._
- **MOD-2** Each model was chosen by running the real task on several candidates and keeping the smallest that passes, and new models face misuse probes before adoption. Verify: the evaluation results. Record the evaluation per role (routing, execution, verification) with cost per 1,000 requests, and include at least one low-cost open-weight candidate. _From R028, R033, R040._
- **MOD-3** Changing facts (prices, policies, specs) come from a maintained document store at answer time, not from fine-tuning; any fine-tuned model beat its base model on a held-out evaluation. Verify: where answers get their facts, and the fine-tune evaluation. A claim that a tuned model knows the business is accepted only if it beats the base model plus retrieval on the same tasks. _From R046._
- **MOD-4** Self-hosted models listen only on a private network behind an authenticating gateway, with no public port or domain. Verify: an external scan and the gateway config. _From R024, R031._
- **MOD-5** Agents and self-hosted models run contained: networking off by default with an allowlist, a non-admin user, a read-only filesystem with one scratch directory, and their own action log. Verify: the container or sandbox config. _From R028, R038._
- **MOD-6** Weights, fine-tuning data, runtime config and keys for self-hosted models live in storage you own, and moving to another host is a scripted, tested procedure. Verify: when the move script last ran. Each fine-tuning run is defined by one versioned config file (dataset version, base model, settings), so any deployed model can be rebuilt from the repository. _From R029, R063._
- **MOD-7** The hosting choice (vendor API, rented servers or owned hardware) is written down with a measured trial of the target model on the real workload and a memory estimate. Verify: the trial numbers. Include a one- to two-year cost comparison at measured volume (API fees against compute, operations time, redundancy and the measured quality gap), record whether the load is steady or bursty, and recheck when pricing or usage changes. _From R015, R031, R040, R055._
- **MOD-8** A license register covers every model in use: attribution, revenue or user caps, and use restrictions. Verify: compare the register with the models in config. _From R033._
- **MOD-9** Each AI provider has a written exit plan: which jobs it runs, where the data lives, how to export it, and the fallback. Verify: the plan and the last time a workflow actually moved. _From R023, R041._
- **MOD-10** Latency-sensitive AI (voice, live chat) streams every stage and has a measured end-to-end latency budget. Verify: latency measured under load. _From R021._
- **MOD-11** Every self-hosted model server runs under a supervisor with a health check that restarts it on failure, and errors, latency, crashes and restarts are monitored with alerts. Verify: kill the inference process on a test host and confirm it restarts and alerts. _From R029, R031._

## Vendors and AI agencies (VEN)
<!-- short: vendors -->

- **VEN-1** Ask every AI vendor what they did before. Look for a track record of deploying software into companies: onboarding, training, change management, multi-year support. Confirm a registered business and current liability insurance, and ask who pays the advisor (commissions, referral fees, vendor ownership); paid recommendations are sales. Ask for named production systems the vendor launched at least three months ago and still supports (with monitoring and incident history), measured results, and any litigation or early terminations. _From R002, R018, R041._
- **VEN-2** Talk to a customer who has worked with them for more than a year before signing. Get three client references with phone numbers and call them; testimonials and case-study pages don't count. _From R002._
- **VEN-3** Know who patches, monitors and supports the agent in year two and during an outage, and give vendors least-privilege access with their own credentials. _From R002._
- **VEN-4** Any vendor-built system survives firing the vendor: code, hosting, domains, databases and model or API accounts are owned by the business, which can run, deploy and change it with the vendor's access revoked. Verify: list each asset's account owner. _From R012._
- **VEN-5** Before any vendor, consultant or AI tool connects to email, file storage or the CRM, a written note states what data it reads, where the data goes, and who signed off. Verify: match connected apps to sign-offs. It also records the provider's terms on training with your data, notice for price changes, and how data is exported if you leave. _From R041, R051._
- **VEN-6** A system inventory lists every third-party tool with owner, workflow, data held and export path, and seats unused for 60 days are removed. Verify: export user lists with last sign-in dates. Each entry records annual cost, renewal date, features actually used and overlaps, with a keep, consolidate, replace or build decision made before each renewal. _From R039._

## Evidence and recoverability (EVI)
<!-- short: evidence & recovery -->

- **EVI-1** Keep a dated register of every AI system and automation: what it does, the data it touches, who built it, who owns it now, and the last independent review with its reviewer. Include staff-adopted AI tools and personal accounts, and for each agent its named owner, written limits and how to shut it off. Record which decisions each agent may take without a human and how its output is verified. _From R006, R035, R053._
- **EVI-2** Access is provable: 2FA on every account, no shared passwords, agents on their own service credentials. Export the list and flag gaps. Include third-party app grants (OAuth) with approver, scopes and last use. _From R006, R022._
- **EVI-3** Logging and retention are confirmed per system, and a one-page incident and recovery summary records the date and result of the last drill. _From R006._
- **EVI-4** You know what your business insurance says about AI, and what the insurer would need to see to cover it; the evidence file is built to that list. Insurers exclude what they can't see, so being easy to underwrite (who built it, how it was reviewed, how access is controlled, how it recovers) is the strategy. _From R008._

## Tenant isolation (TEN)
<!-- short: tenant isolation -->

For any product that serves more than one customer from the same system.

- **TEN-1** The tenant model is chosen on purpose and written down: a separate database or stack per customer, or shared tables where every row carries a customer ID. Verify: the document exists and matches the schema. _From R010._
- **TEN-2** Isolation is enforced below the app: database row-level security or separate credentials per customer, so a query without the right customer context returns nothing even when the code is wrong. A filter in app code alone is not isolation. _From R010._
- **TEN-3** Every release runs automated cross-tenant attacks: sign in as one test customer and try to read, change and export another customer's data through every screen and API (changed IDs, direct API calls, exports). Any success fails the release. Add a per-query test proving every data-access path filters by the calling customer. _From R010, R027._

## Change control for in-house builders (CHG)
<!-- short: change control -->

- **CHG-1** Every tool or automation staff build lives in one company repository under company accounts with 2FA, never on a personal laptop or account, so the tool stays when the person leaves. Verify: list staff-built scripts and automations and where each one lives. _From R009._
- **CHG-2** Builders work against realistic sample data generated from the real schema (no real names, numbers or addresses); real data stays behind review. Verify: the build environment has no path to production data. _From R009._
- **CHG-3** The main branch is protected: every change goes through a pull request with automatic secret scanning and one named reviewer, and every release logs who approved it. Changes touching money, customer records or personal data need a named production approver, and agents can't merge their own changes. _From R009, R054._
- **CHG-4** AI-generated code is marked in commit or pull-request metadata, and each such change has a named human owner. Verify: sample recent merges. _From R054._
- **CHG-5** A written list names who may build AI tools and automations and the sanctioned environment for each. Verify: compare it with what is actually running. _From R009._

## Business viability (BIZ)
<!-- short: business viability -->

- **BIZ-1** Someone is paying, or has committed to pay, for the problem this product solves. Without that it's a project, not a business. Verify: name the paying customers or signed pre-orders. A paid pilot counts; customer-funded deals state in writing who owns the code and IP and whether it can be resold. _From R011, R016, R049._
- **BIZ-2** The product answers "why wouldn't the customer build this themselves with the same AI tools?": it saves them time, brings engineering they don't have, or takes accountability when it breaks. Verify: support, uptime and incident commitments are written down and met. Name who answers lockouts and outages after hours and the response times; route monitoring alerts to a named on-call person with a runbook someone else can follow; name the decision logic rivals can't buy off the shelf. _From R011, R026, R027._
- **BIZ-3** An independent security and production-readiness review is done before the first paying customer signs. Verify: a dated review and its fixes. _From R027._

## Automation rollout (ROLL)
<!-- short: automation rollout -->

- **ROLL-1** A process is written down (including manual checks and unwritten know-how) and its data cleaned before it is automated. Verify: the process document predates the automation. The target workflow starts from the outcome, names which steps the AI owns, and lists the exceptions that escalate to a named person. _From R036._
- **ROLL-2** The first automation is chosen with a written rationale: a foundation others depend on, a fixed deadline, or measurable proof. Verify: the rationale exists. _From R019._
- **ROLL-3** A new automated process replaces the old one only after a shadow run on live data with daily comparison. Verify: the shadow logs and the cutover decision. Data reaches the new system through repeatable connectors that clean records and log rejected rows, and the old system stays live until the new one has handled the full workload for an agreed period. _From R042._
- **ROLL-4** Every AI rollout names the workflow it changes, with baseline and after measurements (hours, error rate, cycle time) rather than seat counts. Verify: the before and after numbers. _From R043._

## User communication and trust (COM)
<!-- short: user trust -->

- **COM-1** The product delivers its core value up front; it doesn't hide it behind engagement tricks (forced follows, "reply with a keyword", fake urgency or other dark patterns). Verify: walk the onboarding, sharing and upgrade flows and list every step that gates value on engagement. _From R003._
- **COM-2** Conversations with users stay real: AI or automated replies are labelled as automated and can hand off to a person. Verify: find every support, chat, email and DM automation and check that it's disclosed and has a handoff path. _From R003._
- **COM-3** Abuse is handled without feeding it: users can block and report, and admins can hide or remove bad-faith content quickly. Verify: find the block, report and remove paths and who can use them. _From R003._
